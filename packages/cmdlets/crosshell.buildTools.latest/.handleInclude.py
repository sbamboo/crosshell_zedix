import json
import os
import shutil
import subprocess

def download_packages(include_file: str, output_dir: str):
    """
    Download and install the packages specified in the include.json file, creating wheels or source distributions as necessary.

    Args:
        include_file (str): The path to the include.json file.
        output_dir (str): The directory where the packages should be saved.
    """
    # Load the include.json file
    with open(include_file, "r") as f:
        include_data = json.load(f)

    # Copy the include.json file to the output directory
    shutil.copy(include_file, output_dir)

    # Write the requirements.txt file
    requirements_file = os.path.join(output_dir, "requirements.txt")
    with open(requirements_file, "w") as f:
        for package, version_info in include_data["Requirements"].items():
            package_version = version_info["Ver"]
            package_type = version_info.get("Type", "None")
            f.write(f"{package}=={package_version}\n")

            # Create a wheel or source distribution as necessary
            if package_type == "Wheel":
                subprocess.run(["pip", "wheel", f"{package}=={package_version}", "--wheel-dir", output_dir])
            elif package_type == "Source":
                subprocess.run(["pip", "download", "--no-binary", ":all:", f"{package}=={package_version}", "-d", output_dir])
            elif package_type == "Egg":
                subprocess.run(["pip", "download", "--no-binary", ":all:", f"{package}=={package_version}", "--egg", "-d", output_dir])
