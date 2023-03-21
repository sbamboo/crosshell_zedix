# Function
import math
def heron_formula(a, b, c):
    # Calculate the semiperimeter
    s = (a + b + c) / 2
    
    # Calculate the area using Heron's formula
    area = math.sqrt(s * (s - a) * (s - b) * (s - c))
    
    # Return the area
    return area


# Get input
a,b,c = float(argv[0]),float(argv[1]),float(argv[2])

print(heron_formula(a,b,c))