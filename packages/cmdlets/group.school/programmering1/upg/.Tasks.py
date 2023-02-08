from random import randint


# [Helper class for the tasks]
class Helpers:
    # Function to get numeral values
    def GetNumeralValue(times=1,msgList=list()):
        returns = []
        if msgList == None or msgList == list() or len(msgList) == 0:
            for _ in range(times):
                msgList.append("Input Value: ")
        for i in range(times):
            while True:
                inp = input(msgList[i])
                if inp == "exit": exit()
                try:
                    value = float(inp)
                    break
                except: pass
            returns.append(value)
        if len(returns) > 1:
            return (*returns,)
        else: return returns[0]

    # Function to get string values
    def GetStringValue(times=1,msgList=list()):
        returns = []
        if msgList == None or msgList == list() or len(msgList) == 0:
            for _ in range(times):
                msgList.append("Input String: ")
        for i in range(times):
            while True:
                inp = input(msgList[i])
                if inp == "exit": exit()
                try:
                    value = str(inp)
                    break
                except: pass
            returns.append(value)
        if len(returns) > 1:
            return (*returns,)
        else: return returns[0]

    # Function to check range containment
    def is_included(range_a, range_b):
        start_a, end_a = range_a
        start_b, end_b = range_b
        return start_a >= start_b and end_a <= end_b

    

# [Upgs (Used classes to group stuff together)]

# Algorithmic code
class Algorithms:
    
    # First
    def one():
        r1,r2 = Helpers.GetNumeralValue(2)
        calculated_resistance = (r1*r2)/(r1+r2)
        print(f"Result: {calculated_resistance}")
    
    # Second
    def two():
        v = Helpers.GetNumeralValue(msgList=["Velocity of car (km/h): "])
        s=v/4+(v**2)/125
        print(f"Result: {s}")

    def two2():
        v,t = Helpers.GetNumeralValue(2,msgList=["Velocity of car (km/h): ","Reactiontime (s): "])
        rs = v/t
        s=rs/4+(v**2)/125
        print(f"Result: {s}")

    # Third
    def three():
        year = Helpers.GetNumeralValue()
        if year/4 == year//4:
            print(True)
        else:
            print(False)
        

# Efficient code
class Efficient:

    # First
    def one():
        seconds = Helpers.GetNumeralValue(msgList=["Seconds: "])
        print(f"Seconds: {seconds}, minutes: {seconds/60}, hours: {seconds/3600}")


    # Second
    def two():
        print(randint(1,20))

    # Third
    def three():
        # Reset counter
        timesThreeNumbers = 0
        # Presets
        lastnum = 0
        lastlastnum = 0
        # Loop
        for _ in range(1000):
            ran = randint(1,6)
            # Found match
            if ran == lastnum and lastnum == lastlastnum:
                timesThreeNumbers += 1
            # Shift al positions
            if lastnum != int():
                lastlastnum = lastnum
            lastnum = ran
        # Print result
        print( timesThreeNumbers )


# Formatting code
class Formatting:

    # First
    def one():
        # Get values
        min = Helpers.GetNumeralValue(msgList=["Minimum value: "])
        max = Helpers.GetNumeralValue(msgList=["Maximum value: "])
        print("\033[94mConversion table\033[0m")
        for num in range(int(min), int(max)):
            print(f"Celcius: {5/9*(num-32)}, Farenheit: {num}")

    # Second
    def two():
        start = Helpers.GetNumeralValue(msgList=["Start of pass (integer): "])
        end = Helpers.GetNumeralValue(msgList=["End of pass (integer): "])
        # Make values int
        start = int(start)
        end = int(end)
        # List of al hours in the pass
        hours_list = []
        for i in range(start,end+1): hours_list.append(i)
        # Increse total procentage
        total_procentage = 0
        range1 = range(0,5+1)
        range2 = range(5,8+1)
        range3 = range(17,20+1)
        range4 = range(20,24+1)
        for i in range1:
            if i in hours_list:
                total_procentage += 100
                break
        for i in range2:
            if i in hours_list:
                total_procentage += 50
                break
        for i in range3:
            if i in hours_list:
                total_procentage += 50
                break
        for i in range4:
            if i in hours_list:
                total_procentage += 100
                break
        # Give result
        print(f"The total precentage of addpay is '{total_procentage}' for '{start} to {end}'")


# Functions code
class Functions:

    # First
    def _one_RandomGen(min=int(),max=int()):
        print(min,max)
        return randint(min,max)
    
    def one(min,max):
        numbers = []
        min = Helpers.GetNumeralValue(msgList=["Minimum value: "])
        max = Helpers.GetNumeralValue(msgList=["Maximum value: "])
        for _ in range(min,max):
            numbers.append(Functions._one_RandomGen(min,max))
        print(numbers)

    # Second
    def _two_IsPrime(n=int()):
        # Must be above 1
        if n <= 1:
            return False
        # Calculate sqrt(n) and only check upto that (Efficieny fix)
        for i in range(2, int(n**(1/2)) + 1):
            # Check for a zero reminder of n/i using modulo to check if the number is divisable by the number we are trying.
            if n % i == 0:
                return False
        return True

    def two():
        largestPrime = 0
        for num in reversed(range(10000)):
            if Functions._two_IsPrime(num):
                largestPrime = num
                break
        print(largestPrime)

