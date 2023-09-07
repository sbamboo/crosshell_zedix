# This script should be run before schedules will work

import os
import sys
import platform
import getpass
import subprocess

def main():

    # Arguments
    if "--anyplatform" in sys.argv:
        sys.argv.pop(sys.argv.index("--anyplatform"))
        anyplatform == True
    else:
        anyplatform == False
    if "--nosudo" in sys.argv:
        sys.argv.pop(sys.argv.index("--nosudo"))
        nosudo == True
    else:
        nosudo == False
    if "-script" in sys.argv:
        i = sys.argv.index("-script")
        script == sys.argv[i+1]
        sys.argv.pop(i+1)
        sys.argv.pop(i)
    else:
        script == None

    print("For info abt this script look at readme.txt")

    # Windows platform message
    if platform.system() == "Windows" and anyplatform == False:
        print("This script only needs to run on Unix based systems! (that uses 'cron')")
        exit()

    # Non sudo
    if os.geteuid() != 0 and nosudo == False:
        print("This script must be run with elevated privileges. (Please run as a sudouser or root)")
        exit()

    # Get script
    if script == None:
        script = input("Script that you have scheduled: ")

    # Add user to the crontab group
    subprocess.run(f"sudo usermod -a -G crontab {getpass.getuser()}", shell=True, check=True)

    # Ensure that the cron service is running
    subprocess.run(f"sudo service cron start", shell=True, check=True)

    # Ensure executionPermission of the scheduled file
    subprocess.run(f"sudo chmod +x {script}", shell=True, check=True)

    print("Done!")

if __name__ == "__main__":
    main()