# ----------------------------------------------------------------------------------------------------------------

# NOTE: To use please use the 'parse_interval_and_generate_schedule' function with the correct arguments, or use cliWrapper.py.
# NOTE: Please read ./readme.txt

# ----------------------------------------------------------------------------------------------------------------


# Imports
import os
import platform
import json
from crontab import CronTab
from _winSchedule import _parse_interval_and_schedule_task_win
from _crontabExpressionGenerator import generate_cron_expression as crontab_expression_generator

parentPath = os.path.abspath(os.path.dirname(__file__))
tasks_file = os.path.join( os.path.abspath(os.path.dirname(__file__)), "tasks.json" )

def nstr(_str):
    if _str == None: return ""
    else: return str(_str)

# Get platform and run a scheduleGenerator
def parse_interval_and_generate_schedule(task_name=str, interval_str=str, script_path=str, script_args=None, python_path=str, python_args=None, break_file_path=None):
    # Add task to tasks.json
    _dict = json.loads(open(tasks_file,'r').read())
    taskNames = []
    for task in _dict["tasks"]:
        taskNames.append(task["name"])
    if task_name in taskNames:
        raise Exception(f"Task {task_name}, is already scheduled! (This only convers tasks scheduled with this library!)")
    else:
        taskData = {"name":task_name, "platform":platform.system(), "interval":interval_str, "script":f"{nstr(script_path)} {nstr(script_args)}","python":f"{nstr(python_path)} {nstr(python_args)}","break_file_path":break_file_path}
        _dict["tasks"].append(taskData)
    _json = json.dumps(_dict)
    open(tasks_file,'w').write(_json)

    # Convert interval string
    interval_int, time_unit_in_seconds = _parse_interval_string(interval_str)

    if platform.system() == "Windows":
        _parse_interval_and_schedule_task_win(task_name, interval_str, script_path, script_args, python_path, python_args, break_file_path)
    elif platform.system() == "Linux" or platform.system() == "Darwin":  # Unix-like systems
        _generate_cron_schedule(task_name, interval_int, interval_str, time_unit_in_seconds, script_path, script_args, python_path, python_args, break_file_path)
    else:
        print("Unsupported platform. Only Windows, Linux, and macOS are supported.")

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

# Generate a schedule file for the cron library using the 'crontab' python modules.
def _generate_cron_schedule(task_name=str, interval_int=int, interval_str=str, time_unit_in_seconds=int, script_path=str, script_args="", python_path=str, python_args="", break_file_path=None):
    # To short interval?
    minutes = interval_int * (time_unit_in_seconds // 60)
    if minutes < 1:
        choice = input("Interval is lower then the recomended interval (1 minute), do you want to start a loopExecution of the file? [y/n] ")
        if choice.lower() == "y":
            _loop_execute_python_file(minutes,break_file_path)
        else:
            raise ValueError("Interval is too short for Task Scheduler. Try again and start a loopExecutionCycle for smaller intervals.")
    else:
        # Convert to cron expression
        cron_expression = crontab_expression_generator(interval_int, interval_str)
        command = str(python_path)
        if python_args != None: command += f" {python_args}"
        if script_path != None: command += f" {script_path}"
        if script_args != None: command += f" {script_args}"
        comment = task_name
        cron = CronTab(user=True)
        job = cron.new(command=command, comment=comment)
        job.setall(cron_expression)
        # Schedule
        cron.write_to_user()

# cron has a not-so-readable format so lets convert things
def _calculate_cron_expression(interval_int, time_unit_in_seconds):
    cron_expression = f"*/{interval_int} * * * *"
    return cron_expression

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