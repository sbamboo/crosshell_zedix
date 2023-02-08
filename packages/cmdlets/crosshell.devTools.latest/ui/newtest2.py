import sys
import subprocess
import wx
import os
from ansimarkup import parse

class MainWindow(wx.Frame):
    def __init__(self):
        super().__init__(None, title="My Console Alternative")
        self.input_field = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.input_field.Bind(wx.EVT_TEXT_ENTER, self.run_command)
        self.output_field = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)

    def run_command(self, event):
        cmd = self.input_field.GetValue()
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
        command = f'python3 {path} "{params}"'
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        output = proc.stdout.read().decode('utf-8')
        formatted_output = parse(output)
        self.output_field.SetValue(formatted_output)

app = wx.App()
window = MainWindow()
window.Show()
app.MainLoop()
