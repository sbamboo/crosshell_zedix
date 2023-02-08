# [Imports]
import assets.lib.importa as im
tasks = im.fromPath(f"{CSScriptRoot}\.Tasks.py")

# Code:

StringToRun = argv[0]
exec(f"tasks.{StringToRun}")