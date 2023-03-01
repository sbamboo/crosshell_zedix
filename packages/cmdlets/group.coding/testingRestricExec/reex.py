# Import
import os
from assets.lib.limitExec import LimitedExec

# Define allowed functions & variables
local_vars = {
    'print': print,
    'str': str,
    'float': float,
    'int': int,
    'bool': bool
}

# Define which variables I want returned
return_scope = {
    "myvar": None
}


# Execute .code.py
return_scope = LimitedExec(f"{CSScriptRoot}{os.sep}.code.py",local_vars,return_scope)

# Print result
print(return_scope)