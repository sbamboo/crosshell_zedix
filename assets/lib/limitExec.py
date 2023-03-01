# LimitExec: Library to limit the capabilities of an executed script
# Author: Simon Kalmi Claesson

# [imports]
import os

# [Dummy classes]
class DummyObject:
    # Subscribable
    def __getitem__(self, key):
        return DummyObject()
    # Callable
    def __call__(self, *args, **kwargs):
        pass

class ReturningDummyObject:
    # Subscribable
    def __getitem__(self, key):
        return key
    # Callable
    def __call__(self, *args, **kwargs):
        return args, kwargs
    
class RaisingDummyObject:
    # Subscribable
    def __getitem__(self, key):
        raise NameError("Callable '"+key+"' Not found in restricted session.")
    # Callable
    def __call__(self, *args, **kwargs):
        raise NameError()

# [Functions]
def LimitedExec(path,allowed_locals,return_scope,mode=None):
    # Get code content
    code = open(path,'r').read()
    # Specify Dummys for blocked sents
    allowed_globals = {
        '__builtins__': DummyObject(),
        '__import__': DummyObject()
    }
    # Overwrite dummys depending on mode
    if mode == "strict": allowed_globals = {'__builtins__': RaisingDummyObject(), '__import__': RaisingDummyObject()}
    elif mode == "returning": allowed_globals = {'__builtins__': ReturningDummyObject(), '__import__': ReturningDummyObject()}
    #Combine what should be returned with allowed_locals
    allowed_locals = allowed_locals | return_scope
    # Backup previous dictionary
    prev_allowed_locals = allowed_locals.copy()
    # Execute code
    exec(code, allowed_globals, allowed_locals)
    # If Dictionary has changed return any key in return scope
    if str(allowed_locals) != str(prev_allowed_locals) and allowed_locals != None:
        # Retrive keys existing in both dictionaries using two sets
        common_keys = set(allowed_locals.keys()) & set(return_scope.keys())
        # Dictionary Comprehension to return dictionary of all changed keys
        return {key: allowed_locals[key] for key in common_keys}
    # Otherwise return the return scope unchanged
    else:
        return return_scope