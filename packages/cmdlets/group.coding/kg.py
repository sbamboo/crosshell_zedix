# Kurragömma crosshell wrapper
import os
tmp_path = CSScriptRoot + os.sep + ".kurragömma" + os.sep + "main.py"
tmp_params = ' '.join(argv)
os.system(f"python3 {tmp_path} {tmp_params}")