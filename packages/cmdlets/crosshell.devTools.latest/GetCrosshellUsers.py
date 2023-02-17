from assets.lib.pantryapi import pantryapireq
from assets.lib.crypto.aes import *
from getpass import getpass as igp
gcu_ikey = igp("key: ")
gcu_pkey = igp("pantrykey: ")
try:
    gcu_key = GenerateKey(gcu_ikey)
    gcu_rans = pantryapireq(key=gcu_pkey,mode='get',basket='CrosshellVerifierNameList')
    gcu_usd = json.loads(gcu_rans.content.decode())
    gcu_us = encdec_dict(key=gcu_key, dictionary=gcu_usd,mode='dec')
    for gcu_c,gcu_n in gcu_us.items():
        print(f"\033[33m{gcu_n}: \033[34m{gcu_c}\033[0m")
except: pass
gcu_key,gcu_pkey,gcu_rans,gcu_usd,gcu_us,gcu_ikey = None,None,None,None,None,None
try: gcu_c = None
except: pass
try: gcu_n = None
except: pass
