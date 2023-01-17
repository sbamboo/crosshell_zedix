# [Imports]
import os
import platform
import getpass
import argparse
import subprocess

cparser = argparse.ArgumentParser(prog="csdk", description="C-Sharp DevKit", epilog="To create a project use '--new -name <name> -type <type>' or to run a program, '--run -name <name>'")
# Options
cparser.add_argument('--new', dest="new_project", action='store_true', help="Creates a new project")
cparser.add_argument('--run', dest="run_project", action='store_true', help="Builds and runs a new project")
# Arguments
cparser.add_argument('-runscript', dest="dotnet_runScript",  help="Runs a script file with dotnet")
cparser.add_argument('-runstring', dest="dotnet_runString",  help="Runs a string as dotnet source code")
cparser.add_argument('-name', dest="project_name", help="Name of the project")
cparser.add_argument('-type', dest="project_type", help="Type of the project")
# Auto consume remaining arguments
cparser.add_argument('options', nargs='*', help="Al other options (auto consume)")
# Create main arguments object
argus = cparser.parse_args(argv)

# [Setup]
LocalProjectPath = f"{CSScriptRoot}{os.sep}.CSharpProjects"
LocalDotnetPath = f"{CSScriptRoot}{os.sep}.dotnet"
def GetDotnetExecutable():
    winLocalDotnetPath = f"{LocalDotnetPath}{os.sep}windows{os.sep}dotnet.exe"
    macLocalDotnetPath = f"{LocalDotnetPath}{os.sep}macos{os.sep}dotnet"
    lnxLocalDotnetPath = f"{LocalDotnetPath}{os.sep}linux{os.sep}dotnet"
    # Get the current operating system
    current_os = platform.system()
    # return correct path
    if current_os == "Windows":
        result = subprocess.run(f"dotnet --version", shell=True, capture_output=True)
        if result.returncode != 0:
            return winLocalDotnetPath
        else:
            return "dotnet"
    elif current_os == "Darwin":
        result = subprocess.run(f"dotnet --version", shell=True, capture_output=True)
        if result.returncode != 0:
            return macLocalDotnetPath
        else:
            return "dotnet"
    elif current_os == "Linux":
        result = subprocess.run(f"dotnet --version", shell=True, capture_output=True)
        if result.returncode != 0:
            return lnxLocalDotnetPath
        else:
            return "dotnet"


# [Install Dotnet]
globals()["DotnetDevKit_DotnetInstaller_DotnetExecutablePath"] = GetDotnetExecutable()
globals()["DotnetDevKit_DotnetInstaller_LocalDotnetPath"] = LocalDotnetPath
exec(open(f"{CSScriptRoot}/.DotnetInstaller.py").read(),globals())


# [Dotnet RunString]
if argus.dotnet_runString:
    # Execute input string as C# script
    print(str(argus.dotnet_runString))
    output = subprocess.run([GetDotnetExecutable(), "script", "eval", str(argus.dotnet_runString)], capture_output=True, text=True)
    print((output.stdout).strip())

# [Dotnet RunScript]
if argus.dotnet_runScript:
    os.system(f'dotnet script {str(argus.dotnet_runScript)}')

# [New project]
if argus.new_project == True:
    projectPath = LocalProjectPath + os.sep + str(argus.project_name)
    if os.path.exists(projectPath) != True: os.mkdir(projectPath)
    OldPath = os.getcwd()
    os.chdir(projectPath)
    os.system(f"{GetDotnetExecutable()} new {str(argus.project_type)}")
    os.chdir(OldPath)

# [Run project]
if argus.run_project == True:
    projectPath = LocalProjectPath + os.sep + str(argus.project_name)
    if os.path.exists(projectPath) != True: os.mkdir(projectPath)
    OldPath = os.getcwd()
    os.chdir(projectPath)
    os.system(f"{GetDotnetExecutable()} run")
    os.chdir(OldPath)
