#!/usr/bin/env python3
'''vt100 terminal color to tkinter Text widget'''

class VT100:
    def __init__(self, text_wig, string=None):
        self.txtwig = text_wig
        self.i = 0; self.j = 1
        if string:
            self.loadTags()
            self.parser(string)

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

if __name__ == "__main__" :
    import sys
    if len(sys.argv) < 2:
        print("Argument(s) Missing", file=sys.stderr); exit(1);

    import tkinter as tk
    root = tk.Tk()
    import tkinter.font as tkFont
    f = tkFont.Font(family="DejaVuSansMono", size=11)
    text = tk.Text(font=f)
    text.pack(expand=1, fill="both")

    from subprocess import check_output
    #VT100(text, check_output(sys.argv[1:], universal_newlines=True))
    input = ('\n'.join(sys.argv[1:])).strip("\n")
    VT100(text, input)
    root.bind("<Key-Escape>", lambda event: root.quit())
    tk.mainloop()