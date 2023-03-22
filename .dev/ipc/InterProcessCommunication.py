import subprocess

class IPCHost():

    Task = list()
    stripAnsi = False

    intProcess = None

    def __init__(self, Task, stripAnsi=False):
        self.Task = Task
        self.stripAnsi = stripAnsi

    def startSubs(self, universalNewlines=bool()):  
        self.intProcess = subprocess.Popen(
            [*self.Task],
            stdin  = subprocess.PIPE,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            universal_newlines= universalNewlines
        )

    def sendInput(self, input):
        self.intProcess.stdin.write(input)

    def getOutput(self):
        stdout = self.intProcess.stdout.readline()
        stderr = self.intProcess.stderr.readline()
        if stderr != "":
            if self.stripAnsi == True:
                return "Subprocess traceback:\n" + stderr
            else:
                return "\033[91mSubprocess traceback:\n\033[33m" + stderr + "\033[0m"
        else:
            return stdout

class IPCSubs():
    
    sysIn=None
    sysOut=None

    def __init__(self, sysIn, sysOut):
        self.sysIn = sysIn
        self.sysOut = sysOut

    def sendInput(self, input):
        self.sysOut.write(input)

    def getOutput(self):
        lines = list()
        for line in self.sysIn:
            lines.append(line)
        return lines