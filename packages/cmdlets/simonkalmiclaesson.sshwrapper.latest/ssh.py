import os
try:
    os.system(f"ssh {(' '.join(argv)).strip(' ')}")
except:
    print(pt_format(cs_palette,"\033[31mError running ssh, please install ssh on your system.\033[0m"))