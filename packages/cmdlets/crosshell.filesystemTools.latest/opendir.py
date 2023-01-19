try: import distro
except:
    os.system("python3 -m pip install distro")

if IsWindows(): os.system("explorer .")
elif IsMacOS(): os.system("open .")
elif IsLinux():
    #Rassberry pi
    if distro.id() == "raspbian": os.system("pcmanfm .")