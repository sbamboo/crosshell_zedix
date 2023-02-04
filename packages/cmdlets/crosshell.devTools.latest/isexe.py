from assets.lib.filesys import filesys as fs
print( fs.isExecutable((' '.join(argv)).strip(" ")) )