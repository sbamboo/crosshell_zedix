try:
    cmd = (' '.join(argv)).strip(" ")
    os.system(cmd)
except:
    print(pt_format(cs_palette,"\033[31mThere was an error executing the command.\033[0m"))