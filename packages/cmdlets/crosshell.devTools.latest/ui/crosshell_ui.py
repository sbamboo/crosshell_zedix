import tkinter as tk
import subprocess
import colorama

def run_crosshell(input_string):
    colorama.init()  # initialize colorama
    process = subprocess.Popen(
        ['python3', 'crosshell.py', '-fc', input_string],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()
    output = colorama.ansi.strip_ansi_codes(stdout.decode() + stderr.decode())  # strip ANSI codes
    text_box.insert("end", output)

root = tk.Tk()
root.title("CrossShell GUI")
root.geometry("400x400")

text_box = tk.Text(root, height=20, width=50)
text_box.pack()

input_field = tk.Entry(root)
input_field.pack()

submit_button = tk.Button(root, text="Submit", command=lambda: run_crosshell(input_field.get()))
submit_button.pack()

root.mainloop()
