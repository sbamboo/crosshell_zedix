# Simple calculator Allowing for the use of Addition, Subtraction, Multiplication, Division, FloorDivision and Exponents.
# Written by: Simon Kalmi Claesson for a school project and is my own property. You may take inspiration from it but not claim this code as your own. If you want to use my code ask me first.
#
# Parameters:
#  - NoCls: Supresses clearing of screen.
#  - DoDebug: Prints out debug information while running.
#  
#  (Any other parameter passed information is passed as an expression to calculate.)
#
# Obs! Every "# type: ignore" is for vscode ignore
#
# Things to do:
#  - String containg e not floatable message
#  - warn overflow
#  - Add support for nested parentheses
#  - Add support for functions from the math module
#  - Safechecks for nonfull expression "2" or "2+"
#  

# Import modules
import os
import sys
import re
import array
import math
from ast import operator
from operator import index
from itertools import islice

# Params
try:
    if argv != "" and argv != None:
        params_raw = argv
    else:
        params_raw = sys.argv
except:
    params_raw = sys.argv
params_nocls = False
try:
    if "dodebug" in str(params_raw):
        dodebug = True
        params_raw[1] = str(params_raw[1]).replace(" -dodebug","")
        params_raw[1] = str(params_raw[1]).replace("-dodebug ","")
        if "nocls" in str(params_raw):
            params_nocls = True
            params_expression = ""
        elif str(params_raw[1]) != "":
            params_expression = str(params_raw[1])
        else:
            params_expression = ""
    else:
        dodebug = False
        if "nocls" in str(params_raw):
            params_nocls = True
            params_expression = ""
        elif str(params_raw[1]) != "":
            params_expression = str(params_raw[1])
        else:
            params_expression = ""
except:
    params_expression = ""

# Clear the screen if not in parameter mode
if params_expression != "" or params_nocls == True:
    os.system("")  # enables ansi escape characters in terminal
else:
    os.system("CLS")

# Function to get index value of n occurence in array/list
# def nth_index(iterable, value, n):
#     matches = (idx for idx, val in enumerate(iterable) if val == value)
#     return next(islice(matches, n-1, n), None)
def nth_index(iterable, value, n):
    indexes = [index for index, char in enumerate(iterable) if char == value]
    #<result_list> = [<thing_to_return> <loop> <condition>]
    return indexes[n-1]

# Scope function variables
expression = ""
numberList = []
operatorList = []
numberList = []
rebuild_operator = ""
# Function to buildLists
def buildlists(expression,rebuild_operator):
    global numberList
    global operatorList
    # Set and split lists
    oprpattern = r'&|@|\+|-|\*|\/'
    # first minus fix
    if (expression[0] == "-"):
        expression = expression.replace("-","#",1)
    numberList = re.split(oprpattern,expression)
    expression = expression.replace('#',"-")
    numberList[0] = str(numberList[0]).replace('#',"-")
    # change numberList to floats
    floatnumberList = []
    for num in numberList:
        if (rebuild_operator == "-" or rebuild_operator == " - "):
            floatnumberList.append(str(num))
        else:
            floatnumberList.append(str(float(num)))
    numberList = floatnumberList
    operatorList = []
    # Rebuild the operator list
    for ch in list(expression):
        if (ch.isnumeric() != True and ch != "."):
            operatorList += ch
    # Return variables
    return expression

# Function to handleoperations
def handleOperation(operationPlaceholder,operation,expression,dodebug):
    global operatorList
    global numberList
    # Set indexnum
    for operator in operatorList:
        indexnum = 0
        if operator in operatorList:
            indexnum = nth_index(operatorList,operator,1)
        else:
            indexnum = 0
        # Match the operator and get numbers
        if (operator == operationPlaceholder):
            num1 = float(numberList[indexnum])  # type: ignore
            num2 = float(numberList[indexnum+1])  # type: ignore
            # Calulate number and replace the non calulated expression with the calculated one.
            # Divide by zero fix.
            if operation == "/" or operation == "//":
                if num1 == 0 or num2 == 0:
                    return "Undefined_DivideByZero"
            # calculatedNum = eval(str(num1) + operation + str(num2))
            calculatedNum = ""
            if (operation == "**") : calculatedNum = float(num1)**float(num2)
            if (operation == "/") : calculatedNum = float(num1)//float(num2)
            if (operation == "*") : calculatedNum = float(num1)*float(num2)
            if (operation == "//") : calculatedNum = float(num1)/float(num2)
            if (operation == "+") : calculatedNum = float(num1)+float(num2)
            if (operation == "-") : calculatedNum = float(num1)-float(num2)
            checkString = str(num1) + str(operationPlaceholder) + str(num2)
            previousExpression = expression
            expression = expression.replace(checkString,str(calculatedNum),1)
            if (re.search('e', expression)): return expression
            #Debug
            if (dodebug): 
                print("\033[94mContent:         \033[92m" + str(operatorList) + " " + str(numberList) + " " + previousExpression,"\033[m")
                print("\033[94mCalculation:     \033[92m" + str(num1) + " " + str(operation) + " " + str(num2) + " = " + str(calculatedNum),"\033[m")
                print("\033[94mStringHandle:    \033[92min_" + str(indexnum) + "   " + checkString + " >> " + str(calculatedNum) + " == "+ expression + "\033[m\n")
            # Rebuild Lists
            rebuild_operator = operator
            expression = buildlists(expression,rebuild_operator)
    return expression

# Function to evaluate an expression
def evaluate(expr):
    global numberList
    global operatorList
    # Check for "Undefined"
    if "Undefined_DivideByZero" in expr:
        return "Undefined: Divide by zero!"
    elif "Undefined" in expr:
        return "Undefined"
    # Replace expressions with placeholders for effected operations.
    expression = expr
    expression = expression.replace('**',"&")
    expression = expression.replace('^',"&")
    expression = expression.replace('//',"@")
    # first minus fix
    allowedOperatorsList = ["+","-","*","/","&","@"]
    firstChar = expression[0]
    if (firstChar in allowedOperatorsList):
        expression = "0" + expression
    # Build lists
    expression = buildlists(expression,rebuild_operator)

    # Change integers in expression to floats.
    newExpression = ""
    count = 0
    for number in numberList:
        if (number != operatorList[-1] and count < (len(operatorList))):
            # print(numberList,operatorList,number,count) # Testing print...
            newExpression += str(float(number)) + str(operatorList[count])
        count = count+1
    newExpression += numberList[-1]
    expression = newExpression

    if (dodebug):  #Debug lists and expressions.
        print("\033[94;46mInput:           \033[92m" + str(operatorList) + " " + str(numberList) + " " + expression + "\033[0m")

    #Power off
    expression = handleOperation("&","**",expression,dodebug)

    #Multiplication
    expression = handleOperation("*","*",expression,dodebug)

    #Division
    expression = handleOperation("/","/",expression,dodebug)

    #FloorDivision
    expression = handleOperation("@","//",expression,dodebug)

    #Addition
    expression = handleOperation("+","+",expression,dodebug)

    #Subtraction
    expression = handleOperation("-","-",expression,dodebug)

    #Fix final expression
    res = expression
    hasLetter = re.search('[a-zA-Z]', res)
    if (hasLetter):
        res = res.replace("&","^")
        return res
    else:
        return float(res)

# Main ui code (terminal-ui)
if params_expression == "":
    print("\033[34mWrite an expression bellow or write 'exit' bellow to exit.\033[0m")
while (True):
    # Get input if not already given by parameters.
    if params_expression != "":
        strinput = str(params_expression)
    else:
        strinput = str(input("\033[32mExpression: \033[35m"))
    orginput = strinput
    print("\033[1A\033[0m")
    # Handle Exit
    if strinput == "exit":
        break
    # Handle Cls
    if strinput == "cls":
        os.system("CLS")
    else:
        # Negative numbers fix
        if (strinput[0] == "-"):
            strinput = "0" + strinput
        # Parentheses support
        if "(" in strinput:
            # Check for parentheses in the string with a regex pattern and split by it.
            parenthesesArray = re.findall('\((.*?)\)',strinput)  # type: ignore
            # Calulculate al expressions inside a parentheses
            for paranExpr in parenthesesArray:
                checkString = str("(" + paranExpr + ")")
                # Calculate expression inside parentheses
                calcparanString = str(evaluate(str(paranExpr)))
                # Negative numbers fix
                if (calcparanString[0] == "-"):
                    calcparanString = "0" + calcparanString
                # Replace the parentheses-expression with the calculated value of said expression.
                strinput = strinput.replace(checkString,calcparanString)
            #Debug
            if (dodebug):
                print("\033[94mParenthes data: \033[92m", str(strinput), "     ", str(parenthesesArray), "\033[0m")
                print("\033[94mInputs:         \033[92m", orginput, "   ", strinput, "\033[0m\n")

        #Calculate answer and print it out.
        answ = str(evaluate(strinput))
        if "Undefined_DivideByZero" in answ:
            answ = "Undefined: Divide by zero!"
        if "Undefined" in answ or "Error" in answ:
            print("\033[31m" + str(orginput) + " = " + answ + "\033[0m")
        else:
            print("\033[33m" + str(orginput) + " = " + answ + "\033[0m")
        #End if parameter is given
        if params_expression != "":
            break




