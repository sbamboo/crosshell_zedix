import os
prefix = ' '.join(argv[0:]).strip("'")
print(formatPrefix(prefix,True,True,os.getcwd(),globals()))