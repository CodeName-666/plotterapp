


class Test():
    def __init__(self) -> None:
        pass

    @property
    def testProp(self):
        try:
            return self.x
        except: 
            return None

    @testProp.setter
    def testProp(self, val):
        self.x = val



if __name__ == "__main__":
    p = Test()
    p.testProp = 5
    b = p.testProp
    print(b)


