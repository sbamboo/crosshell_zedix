# Crosshell compatability
try:
    crosshell_input = ' '.join(argv)
    crosshell_input = crosshell_input.strip("")
except:
    crosshell_input = ""

if crosshell_input == None or crosshell_input == "":
    inputS = input("Input number:")
else:
    inputS = crosshell_input


# conv to float
try:
    num = float(inputS)
except:
    print("Invalid input")
    num = ""

# Check and run
if num != "" and num != None:
    if num/2 == round(num/2):
        even = True
    else:
        even = False

    # Print
    if even == True:
        print(f"The number {num} is even.")
    elif even == False:
        print(f"The number {num} is not even.")