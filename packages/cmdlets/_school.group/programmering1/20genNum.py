import random
numbers = []
for _ in range(20):
    numbers.append( random.randint(0,999) )

string = ""
for num in numbers:
    string += str(num) + ";"
string = string.strip(";")
print(string)