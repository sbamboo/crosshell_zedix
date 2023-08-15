import os,sys,platform

if platform.system() == "Windows":

    force = False
    if "force" in sys.args.join(" "):
        force = True

    if force != True:
        confirmed = False
        while confirmed != True:
            c = input("Are you sure you want to reboot your computer into bios? [y/n] ")
            if c == True: confirmed = True
    else:
        confirmed = True

    if confirmed == True:
        os.system('cmd.exe /c "shutdown /r /fw /f /t 0"')

else:
    print("This command only supports windows!")