import os
import subprocess
import json

def install_packages(include_file: str, python_path: str):
    """
    Install the packages specified in the include.json file, using the local Python installation specified by python_path.

    Args:
        include_file (str): The path to the include.json file.
        python_path (str): The path to the local Python installation.
    """
    # Load the include.json file
    with open(include_file, "r") as f:
        include_data = json.load(f)

    # Install the specified version of Python
    python_version = include_data["PyVersion"]
    subprocess.run(["python", "-m", "venv", python_path])
    subprocess.run([os.path.join(python_path, "Scripts", "pip"), "install", "--upgrade", "pip"])
    subprocess.run([os.path.join(python_path, "Scripts", "pip"), "install", "wheel"])
    subprocess.run([os.path.join(python_path, "Scripts", "pip"), "install", f"python=={python_version}"])

    # Install the specified packages
    for package, version_info in include_data["Requirements"].items():
        package_version = version_info["Ver"]
        package_type = version_info.get("Type", "None")
        package_path = os.path.join(os.path.dirname(include_file), "compiled")
        if package_type == "Wheel":
            package_file = f"{package}-{package_version}-py3-none-any.whl"
        elif package_type == "Egg":
            package_file = f"{package}-{package_version}-py3.10.egg"
        elif package_type == "Source":
            package_file = f"{package}-{package_version}.tar.gz"
        else:
            continue
        package_path = os.path.join(package_path, package_file)
        subprocess.run([os.path.join(python_path, "Scripts", "pip"), "install", package_path])
