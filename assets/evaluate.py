# [Imports]
import os
from assets.utils.conUtils import *


# [Code]

# function to execute any input string as a crosshell command
def cs_execInput(cmd=str()):
    # Get basedir
    lista = os.path.realpath(__file__).split(os.sep)
    lista.pop(-1)
    path = str(os.sep).join(lista) + f"{os.sep}..{os.sep}"
    # Set path to main file
    mainfile = f"{path}{os.sep}crosshell.py"
    # Call a os.system command which starts the app in a sepparate session to run the command
    os.system(f'python3 "{mainfile}" --nocls --nohead -c "{cmd}" --is_internaly_called')