pyinstaller --onefile --name snake --add-data "themes/*;themes" --add-data "GamehubAPI/*;GamehubAPI" --add-data "API.sconf;." --add-data "banner.ps1;." --add-data "basetheme.xml;." --add-data "snake.ps1;." --add-data "tos.txt;."  --hidden-import requests --hidden-import pyyaml --hidden-import cryptography --hidden-import pyaes --hidden-import scandir --hidden-import uuid --add-data "GamehubAPI/managers/*;GamehubAPI/managers" --add-data "GamehubAPI/internal_services/save/*;GamehubAPI/internal_services/save" --add-data "GamehubAPI/libs/*;GamehubAPI/libs" --add-data "GamehubAPI/libs/libcrypto/*;GamehubAPI/libs/libcrypto" launcher.py
