import os
import platform
import subprocess

# Setup dotnetExecutablePath
import importlib.util
spec = importlib.util.spec_from_file_location(
    name="cssharpdevkit",
    location=f"{CSScriptRoot}/.module.py",
)
csdk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(csdk)

# Check if .NET Core SDK is installed
if os.system(f"{csdk.GetDotnetExecutable()} --version") != 0:
    # Get the current operating system
    current_os = platform.system()

    # Set the temporary path
    temp_path = f"{CSScriptRoot}{os.sep}.temppath"

    # Download and run the correct installer

    # Windows
    if current_os == "Windows":
        os.system(f"powershell Invoke-WebRequest -Uri 'https://dotnet.microsoft.com/download/dotnet-core/thank-you/sdk-5.0.100-windows-x64-installer' -OutFile '{temp_path}\\dotnet.exe'")
        result = subprocess.run(f"{temp_path}\\dotnet.exe", shell=True)
        if result.returncode == 0:
            os.system(f"Remove-Item {temp_path}\\dotnet.exe -Force")
        else:
            print(pt_format(cs_palette,"\033[31mError: Installation of dotnet SDK failed, please manually install the dotnet SDK and runtime and rerun this script!\033[0m"))

    # Macos (Darwin)
    elif current_os == "Darwin":
        os.system(f"curl -o {temp_path}/dotnet-sdk-5.0.100-osx-x64.pkg https://dotnet.microsoft.com/download/dotnet-core/thank-you/sdk-5.0.100-macos-x64-installer")
        result = subprocess.run(f"open {temp_path}/dotnet-sdk-5.0.100-osx-x64.pkg", shell=True)
        if result.returncode == 0:
            os.system(f"rm -r {temp_path}/dotnet-sdk-5.0.100-osx-x64.pkg")
        else:
            print(pt_format(cs_palette,"\033[31mError: Installation of dotnet SDK failed, please manually install the dotnet SDK and runtime and rerun this script!\033[0m"))

    # Linux
    #elif current_os == "Linux":
    #    if os.path.exists(f"{temp_path}{os.sep}dotnet") == False:
    #        os.mkdir(f"{temp_path}{os.sep}dotnet")
    #    os.system(f"wget https://download.visualstudio.microsoft.com/download/pr/c646b288-5d5b-4c9c-a95b-e1fad1c0d95d/e13d71d48b629fe3a85f5676deb09e2d/dotnet-sdk-7.0.102-linux-x64.tar.gz -P {temp_path}")
    #    result = subprocess.run(f"tar -xvf {temp_path}/dotnet-sdk-7.0.102-linux-x64.tar.gz -C {temp_path}/dotnet", shell=True)
    #    if result.returncode == 0:
    #        os.system(f"rm -r {temp_path}/dotnet-sdk-7.0.102-linux-x64.tar.gz")
    #    else:
    #        print(pt_format(cs_palette,"\033[31mError: Installation of dotnet SDK failed, please manually install the dotnet SDK and runtime and rerun this script!\033[0m"))
    elif current_os == "Linux":
        os.system(f"wget https://dot.net/v1/dotnet-install.sh -P {temp_path}; sudo chmod +x {temp_path}/dotnet-install.sh")
        result = subprocess.run(f"{temp_path}/dotnet-install.sh --version latest", shell=True)
        if result.returncode == 0:
            os.system('export PATH="$HOME/.dotnet:$PATH"')
            os.system(f"rm -r {temp_path}/dotnet-install.sh")
        else:
            print(pt_format(cs_palette,"\033[31mError: Installation of dotnet SDK failed, please manually install the dotnet SDK and runtime and rerun this script!\033[0m"))


# Check if dotnet-script package is installed
output = subprocess.run([csdk.GetDotnetExecutable(), "tool", "list", "-g"], capture_output=True, text=True)
if "dotnet-script" not in output.stdout:
    os.system(f"{csdk.GetDotnetExecutable()} tool install -g dotnet-script")