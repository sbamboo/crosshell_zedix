dirIn = ' '.join(argv)
dirIn.strip(" ")

if os.path.exists(dirIn) == True:
    try:
        touchFile(dirIn,"utf-8")
    except:
        print(f"\033[31mError: Could not create file: '{dirIn}'\033[0m")
else:
    print(f"\033[31mError: Could not find file: '{dirIn}'\033[0m")