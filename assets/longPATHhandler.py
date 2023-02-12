import sys
import ctypes
from assets.lib.conUtils import IsWindows

def is_long_path_enabled():
    # Get the full path to the Python executable
    python_exe = sys.executable
    
    # Call the GetLongPathName function to get the long path version of the executable
    long_path = ctypes.create_unicode_buffer(512)
    result = ctypes.windll.kernel32.GetLongPathNameW(python_exe, long_path, len(long_path))
    if result == 0:
        # Error: GetLongPathName failed
        return False
    
    # Check if the long path is longer than the original path
    if len(long_path.value) > len(python_exe):
        # Long path support is enabled
        return True
    else:
        # Long path support is not enabled
        return False

def string_allowed(string):
    # Check if windows otherwise return True
    if IsWindows():
        # Check if long path is enabled and compare string length
        if len(string) >= 32767: return False
    # Non windows return true
    else: return True