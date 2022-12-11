import os
from assets.utils.conUtils import *
def cs_execInput(cmd=str()):
    lista = os.path.realpath(__file__).split(os.sep)
    lista.pop(-1)
    path = str(os.sep).join(lista) + f"{os.sep}..{os.sep}"
    mainfile = f"{path}{os.sep}zedix.py"
    os.system(f'python3 "{mainfile}" --nocls --nohead -c "{cmd}"')