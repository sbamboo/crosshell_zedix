# Add python repository to apt
sudo add-apt-repository ppa:deadsnakes/ppa
# Update list of packages post repository addition
sudo apt-get update
# Install python3 pip3 and powershells pre-requisite packages
sudo apt-get install -y software-properties-common python3 python3-pip xterm wget apt-transport-https
# Download the microsoft repository GPG keys
wget -q "https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/packages-microsoft-prod.deb"
# Register the Microsoft repository GPG keys
sudo dpkg -i packages-microsoft-prod.deb
# Update the list of packages after we added packages.microsoft.com
sudo apt-get update
# Install powershell
sudo apt-get install -y powershell
# Install python deps for crosshell
pip3 install pyyaml
pip3 insyall tqdm
pip3 install requests
pip3 install promt_toolkit
pip3 install pygments
