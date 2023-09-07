import os
import subprocess
import xml.etree.ElementTree as ET
from datetime import datetime
import time

def _loop_execute_python_file(minutes, break_file_path=str):
    # Parse interval
    seconds = minutes * 60
    # Loop and execute
    while True:
        if os.path.exists(break_file_path):
            os.remove(break_file_path)
            break
        else:
            command = str(python_path)
            if python_args != None: command += f" {python_args}"
            if script_path != None: command += f" {script_path}"
            if script_args != None: command += f" {script_args}"
            os.system(command)
            time.sleep(seconds)

#Helper function to convert interval-strings: 10_days = 10, 86400(seconds_in_a_day)
def _parse_interval_string(interval_str):
    interval_str = interval_str.lower()
    time_units = {"minutes": 60, "hours": 3600, "days": 86400, "weeks": 604800, "months": 2592000}
    interval_int = int(interval_str.split('_')[0])
    unit = interval_str.split('_')[1]
    if unit not in time_units:
        raise ValueError("Invalid time unit. Allowed units: minutes, hours, days, weeks, months")
    time_unit_in_seconds = time_units[unit]
    return interval_int, time_unit_in_seconds

# Main windows scheduler function (Use 'pythonw.exe' to run the script without a terminal window)
def _parse_interval_and_schedule_task_win(task_name=str, interval_str=str, script_path=str, script_args="", python_path=str, python_args="", break_file_path=None):
    # Parse interval
    interval_int, time_unit_in_seconds = _parse_interval_string(interval_str)
    # Convert to minutes and define a command
    minutes = interval_int * (time_unit_in_seconds // 60)
    command = str(python_path)
    if python_args != None: command += f" {python_args}"
    if script_path != None: command += f" {script_path}"
    if script_args != None: command += f" {script_args}"
    # In case of too short schedule ask user if should start looping
    if minutes < 1:
        choice = input("Interval is to short for the TaskScheduler, do you want to start a loopExecution of the file? [y/n] ")
        if choice.lower() == "y":
            _loop_execute_python_file(minutes,break_file_path)
        else:
            raise ValueError("Interval is too short for Task Scheduler. Try again and start a loopExecutionCycle for smaller intervals.")
    # Generate the Task Scheduler XML
    task_xml = _generate_task_scheduler_xml(command, minutes)
    # Schedule the task using the generated XML
    _schedule_task_with_xml(task_xml,task_name)


def _generate_task_scheduler_xml(command, interval_in_minutes):
    # split command and arguments
    arguments = (" ".join( command.split(" ")[1:] ) ).strip()
    command = command.split(" ")[0]
    # Get date
    date = datetime.now().strftime("%Y-%m-%d")
    # Generate root xml
    root = ET.Element('Task', xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task")
    registrationInfo = ET.SubElement(root, 'RegistrationInfo')
    triggers = ET.SubElement(root, 'Triggers')
    principal = ET.SubElement(root, 'Principals')
    settings = ET.SubElement(root, 'Settings')
    actions = ET.SubElement(root, 'Actions')
    # Add subelements
    ET.SubElement(settings, 'MultipleInstancesPolicy').text = "IgnoreNew"
    ET.SubElement(settings, 'DisallowStartIfOnBatteries').text = "false"
    ET.SubElement(settings, 'StopIfGoingOnBatteries').text = "false"
    ET.SubElement(settings, 'StartWhenAvailable').text = "false"
    ET.SubElement(settings, 'RunOnlyIfNetworkAvailable').text = "false"
    ET.SubElement(settings, 'IdleSettings').text = ""
    # Add command
    ET.SubElement(actions, 'Exec')
    ET.SubElement(actions.find('Exec'), 'Command').text = command
    ET.SubElement(actions.find('Exec'), 'Arguments').text = arguments
    # Add interval
    ET.SubElement(triggers, 'TimeTrigger')
    ET.SubElement(triggers.find('TimeTrigger'), 'StartBoundary').text = f"{date}T00:00:00"
    ET.SubElement(triggers.find('TimeTrigger'), 'EndBoundary').text = f"9999-12-31T23:59:59"
    ET.SubElement(triggers.find('TimeTrigger'), 'Enabled').text = "true"
    repetition = ET.SubElement(triggers.find('TimeTrigger'), 'Repetition')
    ET.SubElement(repetition, 'Interval').text = f'PT{interval_in_minutes}M'  # PT stands for "Period Time"; M stands for "Minutes"
    ET.SubElement(repetition, 'StopAtDurationEnd').text = 'false'
    # Return XML string
    xml_string = ET.tostring(root).decode()
    return xml_string

def _schedule_task_with_xml(task_xml, task_name=str):
    try:
        # Save the XML to a temporary file
        temp_file_path = "temp_task.xml"
        with open(temp_file_path, "w") as temp_file:
            temp_file.write(task_xml)

        # Use schtasks command to create the scheduled task from the XML file
        subprocess.run(["schtasks", "/Create", "/XML", temp_file_path, "/TN", task_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error creating the scheduled task: {e}")
    finally:
        # Delete the temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
