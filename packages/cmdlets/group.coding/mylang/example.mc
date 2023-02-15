# Comments are not counted with line numbers unless a number is defined
1  print("hello world")
2  # Comments can be on a line 
^  #Lines may start with exponent character to use one line after the above
^  # This behaivor can be stacked
5  # Double space from number to line
10 # You may jump in line numbers arbitrarly
GT: 10 # Define a goto, where the code will goto a line (GT) for goto colon space and the line number
^  # Having a exponent line number past a GT will work since GT works as a exponent in linenumber counting
15 GT: 10 # Note you may also define a line number for a GOTO
16 str.my_string = "hello" # Code works like python but types are defined by "type dot variable name" and types use python names
17  def MyFunction() { # Functions work exactly as in python but instead of colons you have curly brackets
^ 	print(my_string) 
20  }
# In general the language is python just with a linenumber system and change in how you define variable types
