import argparse
import requests

cparser = argparse.ArgumentParser(prog="Packagehand")
# Install
cparser.add_argument('--install','--add','--a', dest="install", action='store_true', help="Install switch")
# Package (Comsume al remaining arguments)
cparser.add_argument('-package','-p', nargs='*', dest="package", help="The package id")
# Create main arguments object
argus = cparser.parse_args(argv)


# Get repo
repository_url = ""
repository = content = (requests.get(repository_url)).text

# Install
if argus.install == True: