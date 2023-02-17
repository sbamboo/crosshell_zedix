class test:
    var = "hello"

    def test(self):
        print(self)

    def test2(self):
        print(self.var)

    def test3():
        print(var)

    def test4():
        print(self.var)

    def test5():
        print(test.var)


eval(f"test.{argv[0]}()")

