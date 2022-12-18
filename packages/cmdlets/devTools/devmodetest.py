# Check devmode
exec(open(os.path.realpath(f"{csbasedir}{os.sep}packages{os.sep}cmdlets{os.sep}devTools{os.sep}.internalDevmodeValidator.py")).read(), globals())
if cs_devmode_valid != True:
    print("\033[31mThis command needs devmode! Please restart crosshell with devmode to run this cmdlet.\033[0m")

# Code
else:
    print(f"Devmode: {cs_devmode_valid}")