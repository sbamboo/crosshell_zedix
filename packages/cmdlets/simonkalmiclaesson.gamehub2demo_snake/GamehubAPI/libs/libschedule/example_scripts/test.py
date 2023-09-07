# [Settings]
customlogfile = None

# [Code]
import os
from datetime import datetime

date = datetime.now().strftime("%Y-%m-%d")

message = f"[{date}]: hello world"

stdlogfile = os.path.join( os.path.abspath(os.path.dirname(__file__)), "out.log")

if customlogfile != None:
  logfile = customlogfile
else:
  logfile = stdlogfile

curContent = ""
if os.path.exists(logfile):
  curContent = open(logfile,"r").read()
  os.remove(logfile)

curContent += f"\n{message}"

open(logfile,"w").write(curContent)
