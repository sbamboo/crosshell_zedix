from schedule import parse_interval_and_generate_schedule
from unschedule import remove_scheduled_task
import argparse

# [Arguments]
cparser = argparse.ArgumentParser(prog="Gamehub_Services_Backup: Cli.py (read libschedule/readme.txt)")
# Options
cparser.add_argument('-task_name', dest="task_name", help="The name of the task.")
cparser.add_argument('-interval_str', dest="interval_str", help="<Interval>_<TimeUnit>, ex: 10_days.")
cparser.add_argument('-script_path', dest="script_path", help="Path to the script to schedule.")
cparser.add_argument('-python_path', dest="python_path", help="Path to the python executable to use. (On windows use pythonw.exe to not create a terminal window)")
cparser.add_argument('-script_args', dest="script_args", help="Aditional Arguments to send to the script. (optional)")
cparser.add_argument('-python_args', dest="python_args", help="Aditional Arguments to send to python. (optional)")
cparser.add_argument('-break_file_path', dest="break_file_path", help="Path to a break-file, if a interval is too short and you need to use a loopExecution cycle provide this. (optional)")
cparser.add_argument('--schedule', dest="schedule", help="Use to schedule a task.",action="store_true")
cparser.add_argument('--unschedule', dest="unschedule", help="Use to unschedule a task.",action="store_true")
# Create main arguments object
argus = cparser.parse_args()

#print(f"[cliWrapper: Start]\nScriptPath: {argus.script_path}\nScriptArgs: {argus.script_args}\nPythonPath: {argus.python_path}\nPythonArgs: {argus.python_args}\n[cliWrapper: End]")

# Execute function
if argus.schedule == True:
    parse_interval_and_generate_schedule(
        task_name=argus.task_name,
        interval_str=argus.interval_str,
        script_path=argus.script_path,
        script_args=argus.script_args,
        python_path=argus.python_path,
        python_args=argus.python_args,
        break_file_path=argus.break_file_path
    )
elif argus.unschedule == True:
    remove_scheduled_task(argus.task_name)
else:
    print("Not action supplied, use --schedule or --unschedule")