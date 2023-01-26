# Imports
import yaml

# Setup
localVersionFile = cs_versionFile
onlineVersionUrl = "https://github.com/simonkalmiclaesson/crosshell_zedix/raw/main/assets/version.yaml"

# Get local version id
with open(localVersionFile, "r") as yamli_file:
    localVersionid = yaml.safe_load(yamli_file)["vid"]
# Get online version id
onlineVersionid = yaml.safe_load(requests.get(onlineVersionUrl).content)["vid"]
# Check if versions needs update
print(localVersionid,onlineVersionid)