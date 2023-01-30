# SimpleErrorHandling: Library to aid with error handling.
# Made by: Simon Kalmi Claesson

class ErrorHandle:

    def IsInt(value):
        try:
            if type(value) == int: return True
            else: return False
        except: return False

    def IsString(value):
        try:
            if type(value) == str: return True
            else: return False
        except: return False

    def IsFloat(value):
        try:
            if type(value) == float: return True
            else: return False
        except: return False

    def IsList(value):
        try:
            if type(value) == list: return True
            else: return False
        except: return False