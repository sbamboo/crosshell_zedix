import os
try:
    dirIn = str(argv[0])
except:
    print("\033[31mInvalid first param\033[0m")

if os.path.exists(dirIn) != True:
    try:
        os.mkdir(dirIn)
    except:
        print(f"\033[31mError: Could not rename directory/file: '{dirIn}'\033[0m")
else:
    print(f"\033[31mError: Directory/File '{dirIn}' aready exists!\033[0m")