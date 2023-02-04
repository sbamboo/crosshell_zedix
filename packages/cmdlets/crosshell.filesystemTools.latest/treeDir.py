import os
dirIn = ' '.join(argv)
dirIn.strip(" ")

if dirIn == "" or dirIn == None:
    dirIn = os.getcwd()

if os.path.exists(dirIn) != True:
    print(f"\033[31mError: Could not find directory/path: '{dirIn}'\033[0m")
    exit()

try:
    for root, dirs, files in os.walk(dirIn, topdown = True):
        for name in files:
            print(os.path.join(root, name))
        for name in dirs:
            print(os.path.join(root, name))
except:
    print(f"\033[31mError: Could not list directory/path: '{dirIn}'\033[0m")