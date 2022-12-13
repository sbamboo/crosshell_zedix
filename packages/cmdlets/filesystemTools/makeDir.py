try:
    dirIn = str(argv[0])
except:
    print("\033[31mInvalid first param\033[0m")
try:
    oper = str(argv[1])
except:
    print("\033[31mInvalid second param\033[0m")

if os.path.exists(dirIn) != True:
    try:
        if oper == "-file":
            touchFile(dirIn,"utf-8")
        elif oper == "-dir":
            os.mkdir(dirIn)
    except:
        print(f"\033[31mError: Could not rename directory/file: '{dirIn}'\033[0m")
else:
    print(f"\033[31mError: Directory/File '{dirIn}' aready exists!\033[0m")