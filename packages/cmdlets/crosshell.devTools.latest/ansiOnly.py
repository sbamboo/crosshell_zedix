ins = ''.join(argv)
ins = ins.replace("\\",'\\')
ins = ins.replace("\\x1b[0M","")
out = ins.split("\\xdb")
out.pop(-1)

print(out)
print(len(out))