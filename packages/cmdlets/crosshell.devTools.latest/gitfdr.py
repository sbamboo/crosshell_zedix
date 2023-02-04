from assets.lib.gitAPI import *
gitFolderDownRecurse((' '.join(argv)).strip(),resultDir=f"{csbasedir}{os.sep}.temp",debug=True)