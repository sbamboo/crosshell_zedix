# [Import]
import os
try:
    import tkinter as tk
except:
    os.system("python3 -m pip install tk")
    import tkinter as tk
try:
    from PIL import Image,ImageTk
except:
    os.system("python3 -m pip install PIL")

# [Files]
try:
    bobFile = CSScriptRoot + os.sep + "bob.png"
except:
    bobFile = os.path.dirname(__file__) + os.sep + "bob.png"

# [Define window]
window = tk.Tk()
window.geometry("400x500")

canvas = tk.Canvas(window, width="400", height="500",background="darkblue")
canvas.pack()
canvas.create_rectangle(0,500, 400,300, fill="darkgreen")
canvas.create_oval(300,100,325,125,fill="yellow")

square = None
bob = None

img = ImageTk.PhotoImage(Image.open(bobFile))

def KeyPressed(e):
    global square,bob
    try:
        square = canvas.create_rectangle(100,300,200,200,fill="red")
        canvas.delete(bob)
    except: pass

def KeyReleased(e):
    global square,bob,img
    try:
        bob = canvas.create_image(100,100,anchor=tk.NW,image=img)
        canvas.delete(square)
    except: pass

window.bind('<KeyPress>', KeyPressed)
window.bind('<KeyRelease>', KeyReleased)

# [Show window]
window.mainloop()