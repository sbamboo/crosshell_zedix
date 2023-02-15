filename = (' '.join(argv)).strip(" ")

f = open(filename,'r')
filecontent = f.read()
f.close()

from assets.lib.importa import fromPath

mylang = fromPath(f"{CSScriptRoot}{os.sep}.translate.py")

pycode = mylang.translate_code(filecontent)

print( pycode )