import os
try:
  import pygments
except:
  os.system("pip3 install pygments")
  import pygments
try:
  import prompt_toolkit
except:
  os.system("pip3 install prompt_toolkit")
  import prompt_toolkit