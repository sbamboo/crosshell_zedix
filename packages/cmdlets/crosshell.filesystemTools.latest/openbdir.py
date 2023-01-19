try: import distro
except:
    os.system("python3 -m pip install distro")

if IsWindows(): os.system(f"explorer {csbasedir}")
elif IsMacOS(): os.system(f"open {csbasedir}")
elif IsLinux():
    #Rassberry pi
    if distro.id() == "raspbian": os.system(f"pcmanfm {csbasedir}")