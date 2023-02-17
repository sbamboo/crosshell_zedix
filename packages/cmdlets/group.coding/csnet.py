try:
    import clr
except:
    os.system("python3 -m pip install pythonnet")
    import clr

def wrapfunc(funcname):
    try:
        clr.AddReference("System.Math")
        from System import Math
        func = getattr(Math, funcname)
        return func
    except:
        raise Exception("The function %s could not be found" % funcname)

pow = wrapfunc("Pow")

print(pow(2,2))
