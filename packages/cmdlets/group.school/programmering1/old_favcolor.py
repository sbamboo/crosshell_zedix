# Import filesys lib/module
from assets.lib.filesys import filesys as fs

# Declare variables
colorfile = f"{fs.getWorkingDir()}{fs.sep}color.txt"
# Check for saved color file
if fs.notExist(colorfile):
    if input("I can't find the memory of your favorite color, Do you want me to remember it? [y/n] ").lower() == "y":
        color = input("Whats your favorite color? ")
        fs.createFile(colorfile)
        fs.writeToFile(color, colorfile)
        print(f"Thanks, i will remember your favorite color {color}!")
else:
    color = fs.readFromFile(colorfile)
    print(f"I remember that your favorite color was: {color}")
    if input("Do you want to change what favorite color i remember? [y/n] ").lower() == "y":
        color = input("Whats your favorite color? ")
        fs.writeToFile(color, colorfile)
        print(f"Thanks, i will remember your favorite color {color}!")
    elif input(f"Do you want me to forget your favorite color? [y/n] ").lower() == "y":
        fs.deleteFile(colorfile)
