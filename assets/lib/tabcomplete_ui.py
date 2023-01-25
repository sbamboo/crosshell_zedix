import os
try:
  from pygments.lexers import PythonLexer
except:
  os.system("pip3 install pygments")
  from pygments.lexers import PythonLexer
try:
  from prompt_toolkit.formatted_text import ANSI
except:
  os.system("pip3 install prompt_toolkit")
  from prompt_toolkit.formatted_text import ANSI

def sInputs_bottom_toolbar():
  return ANSI("\033[32mWrite 'help' for help :)\033[0m")

def sInputs_bottom_toolbar_color():
  return "ansigreen"