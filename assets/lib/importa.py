# Importa: Library to import modules from path
# Made by: Simon Kalmi Claesson
# Version: 1.1

# [imports]
import importlib.util

# [Functions]
def fromPath(path):
    spec = importlib.util.spec_from_file_location("module", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def fromPathAA(path):
    spec = importlib.util.spec_from_file_location("module", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.__dict__