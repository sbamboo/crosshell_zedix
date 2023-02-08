#!/usr/bin/env python3
'''vt100 terminal color to tkinter Text widget'''
import tkinter as tk
import tkinter.font as tkFont
import os

class VT100:
    def __init__(self, text_wig):
        self.txtwig = text_wig
        self.i = 0; self.j = 1
        self.loadTags()
        
    def loadTags(self):
        font_name = self.txtwig['font']
        bold_font = tkFont.nametofont(font_name).copy()
        bold_font.config(weight="bold")
        italic_font = tkFont.nametofont(font_name).copy()
        italic_font.config(slant="italic")
        self.txtwig.tag_config('1', font=bold_font)
        self.txtwig.tag_config('3', font=italic_font)
        self.txtwig.tag_config('4', underline=1)
        self.txtwig.tag_config('9', overstrike=1)
        self.pallet8 = [
            "black", "red", "green", "yellow", "blue", "magenta",
            "cyan", "white", "magic", "default", # magic: enable 256 color
        ]
        for i in range(8): # pallet8
            self.txtwig.tag_config(str(i+30), foreground=self.pallet8[i])
            self.txtwig.tag_config(str(i+40), background=self.pallet8[i])
        pallet16 = [
            "000000","800000","008000","808000","000080","800080","008080","c0c0c0",
            "808080","ff0000","00ff00","ffff00","0000ff","ff00ff","00ffff","ffffff",
        ]
        for i in range(16): # 0-15/256-colors
            self.txtwig.tag_config(str(i)+"fg", foreground="#"+pallet16[i])
            self.txtwig.tag_config(str(i)+"bg", background="#"+pallet16[i])
        xx = [ "00", "5f", "87", "af", "d7", "ff" ]
        for i in range(0, 216): # 16-231/256-colors
            prefix = str(i+16); rgb = "#"+xx[i//36]+xx[(i//6)%6]+xx[i%6]
            self.txtwig.tag_config(prefix+"fg", foreground=rgb)
            self.txtwig.tag_config(prefix+"bg", background=rgb)
        for i in range(24): # 232-255/256-colors
            prefix = str(i+232); rgb = "#"+hex(i*10+8)[2:]*3
            self.txtwig.tag_config(prefix+"fg", foreground=rgb)
            self.txtwig.tag_config(prefix+"bg", background=rgb)

    def tagSGR(self, code):
        if code == "": return
        if   self.ext == "485": code += "bg"; self.ext = ""
        elif self.ext == "385": code += "fg"; self.ext = ""
        elif self.ext: self.ext += code; return; # 2nd skip
        elif code in [ "38", "48" ]: self.ext = code; return;
        else: code = int(code) # escape precision ie. 01
        if code == 0: return # ignore 0
        self.txtwig.tag_add(code, self.pre, self.cur)
        return code

    def de_code(self, fp):
        self.ext = ""; fbreak = fp
        while self.string[fp] != 'm':
            if self.string[fp] == ";":
                self.tagSGR(self.string[fbreak:fp])
                fbreak = fp + 1
            fp += 1
        self.tagSGR(self.string[fbreak:fp])

    def parser(self, string):
        self.cur = ""
        fp = cflag = code = 0
        length = len(string)
        self.string = string
        while fp < length:
            if string[fp]=='\x1b':
                self.pre = self.cur
                self.cur = str(self.j) + '.' +str(self.i) #self.txtwig.index(tk.CURRENT)
                pcode = code; code = fp + 2 # +2 shift escape sequence
                while string[fp] != "m": fp += 1
                fp += 1; cflag += 1
                if cflag == 2:
                    self.de_code(pcode); cflag -= 1;
                continue
            if string[fp] == '\n': self.j += 1; self.i = -1
            self.txtwig.insert("end", string[fp])
            fp += 1; self.i += 1

import subprocess

def run_command():
    # Function to get input from user and send it as an argument to crosshell command
    input_value = text_box.get("1.0",'end-1c')
    process = subprocess.Popen(["C:\Users\simonkalmi.claesson\Documents\Github\crosshell_zedix\crosshell.py", "-a", "CdBdir"], stdout=subprocess.PIPE)
    stdout, _ = process.communicate()
    output = stdout.decode("utf-8")
    vt = VT100(text_box, string=output)
    vt.parser(output)

root = tk.Tk()
root.geometry("400x400")
text_box = tk.Text(root, bg="black", fg="white")
text_box.pack(fill="both", expand=True)
text_input = tk.Entry(root)
text_input.pack()
text_input.bind("<Return>", lambda e: run_command())
root.mainloop()
