from assets.lib.crypto import encdec
KRYPTOKEY = GenerateKey("CROSSHELL VERIFIER TOOLKIT jja18aj1a SIGNED IT BIT")
string = 'c96b7120-d350-4ac1-af69-1bee5f3554d3'


ret = encdec(key=KRYPTOKEY,inputs=string,mode='enc')
print(ret)