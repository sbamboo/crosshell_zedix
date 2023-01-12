# OBS! I am using a temporary variable named "valid" to check whether or not the input is valid, this is instead of for example using exit() since I want this code to be able to run in my crosshell app for testing.

# Imports
import random as ran
import os

# Enable ANSI on windows
os.system("")

# Get input from the user
numsString = input("\033[32mWrite 20 numbers separeated by semicolons, write nothing to automise user input: \033[0m")

# Check for debug
debug = False
if "-debug" in numsString:
    debug = True
    numsString = numsString.replace("-debug", "")

# Randomise 20 numbers if input is empty
if numsString == "" or numsString == None:
    numbers = []
    for _ in range(20):
        numbers.append( ran.randint(0,999) )
# Split user string by semicolons
else:
    if ";" in numsString:
        numbers = numsString.split(";")
    else:
        print("\033[31mError: No semicol found in input!\033[0m")

if debug: print(f"Numbers: {numbers}")# DEBUG

# Validate input to contain semicolons
valid = False
if len(numbers) < 20:
    print(f"\033[31mError: Please input 20 numbers, only got: {len(numbers)} numbers.\033[0m")
else:
    # Valid input so continue
    valid = True

if debug: print(f"Valid: {valid}")# DEBUG

# Define a function where it generates 100 random numbers gets the max and min of them and matches an inputed number list to them
def randMatchOfNumList(numbers=list(),debug=bool()):
    # Get 100 random numbers
    computer_generated_numbers = []
    for _ in range(100):
        computer_generated_numbers.append( ran.randint(0,999) )
    if debug: print(f"ComputerGeneratedNumbers: {computer_generated_numbers}")# DEBUG
    # Get max of computer_generated_numbers
    max = 0
    for num in computer_generated_numbers:
        if int(num) > max: max = num
    if debug: print(f"Max: {max}")# DEBUG
    # Get min of computer_generated_numbers
    min = 999
    for num in computer_generated_numbers: 
        if int(num) < min: min = num
    if debug: print(f"Min: {min}")# DEBUG
    # Go through all numbers in the numbers list and remove the ones that aren't within the range.
    for num in numbers:
        if not int(num) > min and int(num) < max:
            numbers.remove(num)
    # Return out
    return numbers

# Run if valid
if valid == True:
    # Print results
    print("First run: ",randMatchOfNumList(numbers,debug))
    print("Second run: ",randMatchOfNumList(numbers,debug))