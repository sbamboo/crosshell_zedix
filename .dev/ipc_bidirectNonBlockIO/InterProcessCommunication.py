import subprocess
import threading

class IPCHost():

    Task = list()
    stripAnsi = False

    outBuffer = str()
    errBuffer = str()
    intProcess = None
    outputThread = None

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

        # Start a separate thread to read the subprocess output
        self.outputThread = threading.Thread(target=self.readOutput)
        self.outputThread.start()

    def readOutput(self):
        for line in self.intProcess.stdout:
            self.outBuffer += line

    def sendInput(self, inputStr):
        self.intProcess.stdin.write(inputStr.encode())
        self.intProcess.stdin.flush()

    def getOutput(self):
        if self.errBuffer != "":
            _tmp = self.errBuffer
            self.errBuffer = ""
            if self.stripAnsi == True:
                return "Subprocess traceback:\n" + _tmp
            else:
                return "\033[91mSubprocess traceback:\n\033[33m" + _tmp + "\033[0m"
        else:
            return self.outBuffer


class IPCSubs():
    
    sysIn=None
    sysOut=None

    def __init__(self, sysIn, sysOut):
        self.sysIn = sysIn
        self.sysOut = sysOut

    def sendInput(self, input):
        self.sysOut.write(input)
        self.sysOut.flush()

    def getOutput(self):
        lines = list()
        for line in self.sysIn:
            lines.append(line)
        return lines
