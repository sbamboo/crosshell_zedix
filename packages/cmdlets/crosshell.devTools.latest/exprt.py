import os
import re
try:
    from sympy import symbols, Eq, solve, sympify
except:
    os.system("python3 -m pip install sympy")
    from sympy import symbols, Eq, solve, sympify

string = ((' '.join(argv)).strip(' ')).strip('"')

def solve_equation(equation):
    x = symbols('x')
    equation = re.sub(r"(\d)(x)", r"\1*\2", equation)
    equation = re.sub(r"\^", "**", equation)
    eq = Eq(sympify(equation))
    return solve(eq, x)


def handle_expression(uhexpr):
    if "=" in uhexpr:
        lhs, rhs = uhexpr.split("=")
        lhs = lhs.strip()
        rhs = rhs.strip()
        eq = f"{lhs}-({rhs})"
        solutions = solve_equation(eq)
    else:
        solutions = solve_equation(uhexpr)
    return solutions

def print_solutions(solutions,org_expr):
    # Print answ
    print(pt_format(cs_palette,f"\033[33mAnswear to: {org_expr}\033[0m"))
    for i,solution in enumerate(solutions):
        if i != len(solutions)-1:
            print(pt_format(cs_palette,f"\033[32m{solution}\033[0m\nor:"))
        else:
            print(pt_format(cs_palette,f"\033[32m{solution}\033[0m"))


expr = ""

if string == "" or string == None:
    while "exit" not in expr:
        expr = input("SP > ")
        solutions = handle_expression(expr)
        print_solutions(solutions,expr)
else:
    solutions = handle_expression(string)
    print_solutions(solutions,string)