class ErrorHandle:

    def IsInt(self, value):
        try:
            if type(value) == int: return True
            else: return False
        except: return False

    def IsString(self, value):
        try:
            if type(value) == str: return True
            else: return False
        except: return False

    def IsFloat(self, value):
        try:
            if type(value) == float: return True
            else: return False
        except: return False

    def IsList(self, value):
        try:
            if type(value) == list: return True
            else: return False
        except: return False