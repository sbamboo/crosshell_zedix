valid = False
while valid != True:
    try:
        v = int(input("Velocity of car: "))
        valid = True
    except: pass

s=v/4+(v**2)/125

print(f"Result: {s}")