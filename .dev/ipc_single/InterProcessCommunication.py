import subprocess

class IPCHost():

    Task = list()
    stripAnsi = False

    outBuffer = str()
    errBuffer = str()
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
    
    def sendInput(self, inputStr):
        self.outBuffer, self.errBuffer = self.intProcess.communicate(inputStr.encode())

    def getOutput(self):
        if self.errBuffer.decode() != "":
            _tmp = self.errBuffer.decode()
            self.errBuffer = ""
            if self.stripAnsi == True:
                return "Subprocess traceback:\n" + _tmp
            else:
                return "\033[91mSubprocess traceback:\n\033[33m" + _tmp + "\033[0m"
        else:
            return self.outBuffer.decode()


class IPCSubs():
    
    sysIn=None
    sysOut=None

    def __init__(self, sysIn, sysOut):
        self.sysIn = sysIn
        self.sysOut = sysOut

    def sendInput(self, inputStr):
        self.sysOut.write(inputStr)

    def getOutput(self):
        lines = list()
        for line in self.sysIn:
            lines.append(line)
        return lines