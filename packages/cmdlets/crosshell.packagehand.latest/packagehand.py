# [Imports]
from assets.lib.tqdm_ui import *
import argparse
import requests
import yaml
import os

cparser = argparse.ArgumentParser(prog="Packagehand",exit_on_error=False,add_help=False)
cparser.add_argument('-h', '--help', action='store_true', default=False, help='Shows help menu.')
cparser.add_argument('--exhelp', action='store_true', default=False, help='Shows help then exits.')
# Install
cparser.add_argument('--install','--add','--a', dest="install", action='store_true', help="Install switch")
# Package (Comsume al remaining arguments)
cparser.add_argument('package', nargs='*', help="The package id")
# Create main arguments object
try: argus = cparser.parse_args(argv)
except: argus = cparser.parse_args()
if argus.help: cparser.print_help()
if argus.exhelp: cparser.print_help(); exit()


# Get repo
repository_url = "https://github.com/simonkalmiclaesson/crosshell_zedix/raw/main/packages/cmdlets/crosshell_packagehand/repo.yaml"
repository_data = yaml.load((requests.get(repository_url)).text, Loader=yaml.Loader)

# Install
if argus.install == True:
	name = (argus.package[0]).strip('"')
	package_url = repository_data[name]

	# [Download]
	formatting = "{desc}: {percentage:3.0f}% |{color}{bar}{reset}| {n_fmt}/{total_fmt}  {rate_fmt}{postfix}  [Elap: {elapsed} | ETA: {remaining}]"
	chars = " " + chr(9592) + chr(9473)
	curdir = os.getcwd()
	os.chdir( os.path.realpath(f"{csbasedir}{os.sep}packages{os.sep}cmdlets") )
	if not os.path.exists(name):
		os.mkdir(name)
	os.chdir( os.path.realpath(f"{csbasedir}{os.sep}packages{os.sep}cmdlets{os.sep}{name}") )
	downloadBar(package_url,formatting,chars)
	os.chdir(curdir)