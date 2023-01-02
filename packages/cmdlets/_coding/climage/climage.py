filename = str(' '.join(argv))
try:
  import climage
except:
  os.system("py -m pip install climage")
  import climage

if os.path.exists(filename):
  print( pt_format(cs_palette,climage.convert(filename)) )
else:
  print( pt_format(cs_palette,f"\033[31mError: File '{filename}' not found\033[0m") )