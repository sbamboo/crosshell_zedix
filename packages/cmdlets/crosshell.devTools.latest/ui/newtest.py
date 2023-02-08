import sys
import subprocess
from PyQt5 import QtWidgets, QtGui, QtCore
import os

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.input_field = QtWidgets.QLineEdit(self)
        self.input_field.move(10, 10)
        self.input_field.returnPressed.connect(self.run_command)

        self.output_field = QtWidgets.QTextEdit(self)
        self.output_field.move(10, 50)
        self.output_field.setReadOnly(True)

        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle("My Console Alternative")
        self.show()

    def run_command(self):
        cmd = self.input_field.text()
        path, params = self.parse_command(cmd)
        self.exec_script(path, params)

    def parse_command(self, cmd):
        cmd_parts = cmd.split(" ")
        cmd = cmd_parts[0]
        params = (' '.join(cmd_parts[1:])).strip(" ")
        cmdps = {
            "help": r"C:\Users\simonkalmi.claesson\Documents\Github\crosshell_zedix\packages\cmdlets\crosshell.devTools.latest\ui\testingstuff\.help.py",
            "ansi": r"C:\Users\simonkalmi.claesson\Documents\Github\crosshell_zedix\packages\cmdlets\crosshell.devTools.latest\ui\testingstuff\.ansi.py"
        }
        path = cmdps.get(cmd)
        return path, params

    def exec_script(self, path, params):
        print( f"'{path}'")
        command = f'python3 {path} "{params}"'
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        output = proc.stdout.read().decode('utf-8')
        self.output_field.setPlainText(output)

app = QtWidgets.QApplication([])
window = MainWindow()
sys.exit(app.exec_())
