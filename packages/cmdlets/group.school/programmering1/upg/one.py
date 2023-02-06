valid = False
while valid != True:
    try:
        r1 = int(input("Resistance of first resistor: "))
        valid = True
    except: pass
valid = False
while valid != True:
    try:
        r2 = int(input("Resistance of second resistor: "))
        valid = True
    except: pass
calculated_resistance = (r1*r2)/(r1+r2)
print(f"Result: {calculated_resistance}")