import os
import subprocess

# Setup dotnetExecutablePath
import importlib.util
spec = importlib.util.spec_from_file_location(
    name="cssharpdevkit",
    location=f"{CSScriptRoot}/.module.py",
)
csdk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(csdk)


# Get input string
csharpCode = (" ".join(argv)).strip()


# Execute input string as C# script
output = subprocess.run([csdk.GetDotnetExecutable(), "script", "eval", csharpCode], capture_output=True, text=True)
print((output.stdout).strip())