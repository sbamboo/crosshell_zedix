import platform
import getpass
import os

def GetDotnetExecutable():
    # Get the current operating system
    current_os = platform.system()

    # return correct path
    if current_os == "Windows":
        return "dotnet"
    elif current_os == "Darwin":
        return "dotnet"
    elif current_os == "Linux":
        dotnetInstallScriptDefaultLocation = f"/home/{getpass.getuser()}/.dotnet/dotnet"
        if os.path.exists(dotnetInstallScriptDefaultLocation):
            return dotnetInstallScriptDefaultLocation
        else:
            return "dotnet"

def GetDotnetScriptExecutable():
    # Get the current operating system
    current_os = platform.system()

    # return correct path
    if current_os == "Windows":
        return "dotnet-script"
    elif current_os == "Darwin":
        return "dotnet-script"
    elif current_os == "Linux":
        dotnetInstallScriptDefaultLocation = f"/home/{getpass.getuser()}/.dotnet/tools/dotnet-script"
        if os.path.exists(dotnetInstallScriptDefaultLocation):
            return dotnetInstallScriptDefaultLocation
        else:
            return "dotnet-script"
