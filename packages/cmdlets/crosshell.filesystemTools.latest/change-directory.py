dirIn = ' '.join(argv)
dirIn.strip(" ")
old_dir = csworking_directory

if dirIn == "-":
    if os.path.exists("-") != True:
        dirIn = ".."

if os.path.exists(old_dir) != True:
    print(f"\033[31mError: Could not find directory/path: '{dirIn}'\033[0m")
else:

    try:
        os.chdir(str(dirIn))
        csworking_directory = os.getcwd()
    except:
        print(f"\033[31mError: Could not get to directory/path: '{dirIn}'\033[0m")
        os.chdir(old_dir)