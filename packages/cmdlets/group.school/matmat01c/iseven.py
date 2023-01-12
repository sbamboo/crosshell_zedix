# Crosshell Compatability: This block of code is for handling input from the crosshell app.
try:
    crosshell_input = ' '.join(argv)
    crosshell_input = crosshell_input.strip("")
except:
    crosshell_input = ""

# If not input was given from crosshell ask the user for input using the inputs() function
if crosshell_input == None or crosshell_input == "":
    inputS = input("Input number: ")
else:
    inputS = crosshell_input



# Check and run
if inputS != "" and inputS != None:
    # Input can't be decimal
    if "." in inputS: print("\033[31mDecimal numbers can't be validated!\033[0m")
    else:
        # Validate input
        try:
            num= int(inputS[-1])
            if "." in str(num/2).rstrip(".0"):
                print(f"\033[31m{inputS} is not even.\033[0m")
            else:
                print(f"\033[33m{inputS} is even.\033[0m")
        except:
            print(f"\033[31minput: {inputS} is invalid\033[0m")
