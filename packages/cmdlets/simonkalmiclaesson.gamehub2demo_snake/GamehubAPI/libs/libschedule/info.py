from tabulate import tabulate
import json
import os

parentPath = os.path.abspath(os.path.dirname(__file__))
tasks_file = os.path.join( os.path.abspath(os.path.dirname(__file__)), "tasks.json" )

def main():
    _json = open(tasks_file,'r').read()
    data = json.loads(_json)
    table_data = []
    for item in data["tasks"]:
        table_data.append([
            item["name"],
            item["platform"],
            item["interval"],
            item["script"],
            item["python"],
            item["break_file_path"]
        ])
    # Set the column headers
    headers = ["Name", "Platform", "Interval", "Script", "Python", "Break File Path"]
    # Print
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    main()