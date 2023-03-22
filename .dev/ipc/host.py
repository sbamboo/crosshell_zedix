from InterProcessCommunication import IPCHost

ipc = IPCHost(Task=["python","subs.py"])

ipc.startSubs(universalNewlines=True)

ipc.sendInput("<MSG:1>")

output = ipc.getOutput()


print(output)