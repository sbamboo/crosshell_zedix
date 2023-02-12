from assets.lib.pantryapi import pantryapireq
ans = pantryapireq(key='c96b7120-d350-4ac1-af69-1bee5f3554d3',mode='get',basket='CrosshellVerifierNameList')
print(ans.content.decode())