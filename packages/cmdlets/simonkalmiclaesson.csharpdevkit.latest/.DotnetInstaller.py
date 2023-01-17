import os
import platform
import subprocess

# Setup dotnetExecutablePath (Theese variables are declared in the main csdk.py file)
DotNetExecutablePath = DotnetDevKit_DotnetInstaller_DotnetExecutablePath
temp_path = DotnetDevKit_DotnetInstaller_LocalDotnetPath

# Check if .NET Core SDK is installed using it's errorcode
result = subprocess.run(f"{DotNetExecutablePath} --version", shell=True, capture_output=True)
if result.returncode != 0:
    if os.path.exists(DotNetExecutablePath) != True:
        # Get the current operating system
        current_os = platform.system()

        # Download and run the correct installer using os specific installers and commands

        # Windows
        if current_os == "Windows":
            os.system(f"powershell Invoke-WebRequest -Uri 'https://download.visualstudio.microsoft.com/download/pr/7c869d6e-b49e-4c52-b197-77fca05f0c69/f3b6fb63231c8ed6afc585da090d4595/dotnet-sdk-7.0.102-win-x64.zip' -OutFile '{temp_path}\\dotnet-sdk-7.0.102-win-x64.zip'")
            if os.path.exists(f'{temp_path}{os.sep}windows') != True:
                os.mkdir(f'{temp_path}{os.sep}windows')
            result = subprocess.run(f"Expand-Archive '{temp_path}\\dotnet-sdk-7.0.102-win-x64.zip' -DestinationPath '{temp_path}{os.sep}windows'", shell=True)
            if result.returncode == 0:
                os.system(f"Remove-Item '{temp_path}\\dotnet-sdk-7.0.102-win-x64.zip' -Force")
            else:
                print(pt_format(cs_palette,"\033[31mError: Installation of dotnet SDK failed, please manually install the dotnet SDK and runtime and rerun this script!\033[0m"))

        # Macos (Darwin)
        elif current_os == "Darwin":
            os.system(f"curl -o '{temp_path}/dotnet-sdk-7.0.102-osx-x64.tar.gz' https://download.visualstudio.microsoft.com/download/pr/91c41b31-cf90-4771-934b-6928bbb48aaf/76e95bac2a4cb3fd50c920fd1601527c/dotnet-sdk-7.0.102-osx-x64.tar.gz")
            if os.path.exists(f'{temp_path}{os.sep}macos') != True:
                os.mkdir(f'{temp_path}{os.sep}macos')
            result = subprocess.run(f"tar -xvf '{temp_path}/dotnet-sdk-7.0.102-osx-x64.tar.gz' -C '{temp_path}{os.sep}macos'", shell=True)
            if result.returncode == 0:
                os.system(f"rm -r '{temp_path}/dotnet-sdk-7.0.102-osx-x64.tar.gz'")
            else:
                print(pt_format(cs_palette,"\033[31mError: Installation of dotnet SDK failed, please manually install the dotnet SDK and runtime and rerun this script!\033[0m"))

        # Linux
        elif current_os == "Linux":
            os.system(f"wget https://download.visualstudio.microsoft.com/download/pr/c646b288-5d5b-4c9c-a95b-e1fad1c0d95d/e13d71d48b629fe3a85f5676deb09e2d/dotnet-sdk-7.0.102-linux-x64.tar.gz -P '{temp_path}'")
            if os.path.exists(f'{temp_path}{os.sep}linux') != True:
                os.mkdir(f'{temp_path}{os.sep}linux')
            result = subprocess.run(f"tar -xvf '{temp_path}/dotnet-sdk-7.0.102-linux-x64.tar.gz' -C '{temp_path}{os.sep}linux'", shell=True)
            if result.returncode == 0:
                os.system(f"rm -r '{temp_path}/dotnet-sdk-7.0.102-linux-x64.tar.gz'")
            else:
                print(pt_format(cs_palette,"\033[31mError: Installation of dotnet SDK failed, please manually install the dotnet SDK and runtime and rerun this script!\033[0m"))


# Check if dotnet-script package is installed using the dotnet application
output = subprocess.run([DotNetExecutablePath, "tool", "list", "-g"], capture_output=True, text=True)
if "dotnet-script" not in output.stdout:
    if os.path.exists(f"{temp_path}{os.sep}.tools") != True:
        os.mkdir(f"{temp_path}{os.sep}.tools")
    # install it witht the dotnet application
    os.system(f"{DotNetExecutablePath} tool install -g dotnet-script --tool-path '{temp_path}{os.sep}{str(current_os).lower()}{os.sep}.tools'")