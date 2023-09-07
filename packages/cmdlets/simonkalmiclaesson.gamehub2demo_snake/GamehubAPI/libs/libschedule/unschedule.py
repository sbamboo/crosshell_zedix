import os
import platform
import subprocess
import json
from crontab import CronTab  # You need to install the 'python-crontab' package: pip install python-crontab

def remove_scheduled_task(task_name):
    # Add task to tasks.json
    tasks_file = os.path.join( os.path.abspath(os.path.dirname(__file__)), "tasks.json" )
    _dict = json.loads(open(tasks_file,'r').read())
    taskNames = []
    for task in _dict["tasks"]:
        taskNames.append(task["name"])
    if task_name not in taskNames:
        raise Exception(f"Task {task_name}, has not been scheduled! (This only convers tasks scheduled with this library!)")
    # remove
    if platform.system() == "Windows":
        _remove_task_on_windows(task_name)
    elif platform.system() == "Linux" or platform.system() == "Darwin":  # Unix-like systems
        _remove_task_on_unix(task_name)
    else:
        print("Unsupported platform. Only Windows, Linux, and macOS are supported.")
    # remove from list
    _dict = json.loads(open(tasks_file,'r').read())
    for task in _dict["tasks"]:
        if task["name"] == task_name:
            current_task = task
    index = _dict["tasks"].index(current_task)
    _dict["tasks"].pop(index)
    _json = json.dumps(_dict)
    open(tasks_file,'w').write(_json)

def _remove_task_on_windows(task_name):
    try:
        subprocess.run(["schtasks", "/Delete", "/TN", task_name, "/F"], check=True)
        print(f"Scheduled task '{task_name}' removed successfully on Windows.")
    except subprocess.CalledProcessError as e:
        print(f"Error removing the scheduled task on Windows: {e}")

def _remove_task_on_unix(task_name):
    try:
        cron = CronTab(user=True)
        for job in cron:
            if job.comment == task_name:
                cron.remove(job)
                cron.write_to_user()
                print(f"Scheduled task '{task_name}' removed successfully on Unix-like system.")
                return

        print(f"Scheduled task '{task_name}' not found on Unix-like system.")
    except Exception as e:
        print(f"Error removing the scheduled task on Unix-like system: {e}")

# Example usage:
# remove_scheduled_task("YourTaskName")
