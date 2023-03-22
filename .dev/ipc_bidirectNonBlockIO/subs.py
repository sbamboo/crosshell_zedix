import sys
from InterProcessCommunication import IPCSubs

ipc = IPCSubs(sys.stdin, sys.stdout)

output = ipc.getOutput()

ipc.sendInput("Hello "+' '.join(output)+" i am OTOT")
