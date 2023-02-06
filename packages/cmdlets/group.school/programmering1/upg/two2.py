valid = False
while valid != True:
    try:
        v = int(input("Velocity of car (): "))
        valid = True
    except: pass

valid = False
while valid != True:
    try:
        t = int(input("Reaction time (s): "))
        valid = True
    except: pass

s=(v*t)/4+(v**2)/125

print(f"Result: {s}")