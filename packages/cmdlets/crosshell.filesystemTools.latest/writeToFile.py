from assets.lib.filesys import filesys as fs
if pipeSTDOUT != None and pipeSTDOUT != "":
    fs.writeToFile(pipeSTDOUT,*argv,autocreate=True)
else:
    fs.writeToFile(*argv,autocreate=True)