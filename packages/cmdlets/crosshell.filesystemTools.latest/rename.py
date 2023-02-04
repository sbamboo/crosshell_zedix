import os
try:
    dirIn = str(argv[0])
except:
    print("\033[31mInvalid first param\033[0m")
try:
    newname = str(argv[1])
except:
    print("\033[31mInvalid second param\033[0m")

if os.path.exists(dirIn) == True:
    try:
        os.rename(os.path.realpath(dirIn),os.path.realpath(newname))
    except:
        print(f"\033[31mError: Could not rename directory/file: '{dirIn}'\033[0m")
else:
    print(f"\033[31mError: Could not find directory/file: '{dirIn}'\033[0m")