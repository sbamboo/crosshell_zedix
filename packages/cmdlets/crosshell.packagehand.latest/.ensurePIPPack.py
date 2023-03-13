# Smal module with functions, made by Simon Kalmi Claesson. Version: 1.0
import os

def ensurePipPack(pyBinary=str(),package=str(),flags=None):
    # Ensure flags only list
    if flags != None and type(flags) != list:
        raise TypeError("Flags must be a list")
    # Run 
    cmd = f"{pyBinary} -m pip install {package}"
    if flags != None:
        for flag in flags:
            cmd += " " + flag
    os.system(cmd)

def pipi(pyBinary,arguments):
    cmd = str(pyBinary) + " -m pip " + str(arguments)
    os.system(cmd)