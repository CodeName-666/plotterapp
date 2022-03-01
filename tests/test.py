


class Test():
    def __init__(self) -> None:
        self.__private_member = 10


    def get(self):
        return self.__private_member


    @property
    def testProp(self):
        try:
            return self.x
        except: 
            return None

    @testProp.setter
    def testProp(self, val):
        self.x = val

    @property
    def secProp(self):
        try:
            return self.y
        except:
            return None

    @secProp.setter
    def secProp(self, val: int):
        try:
            self.y.append(val)
        except:
            self.y = list()
            self.y.append(val)

if __name__ == "__main__":
    p = Test()
    p.testProp = 5
    b = p.testProp
    print("Member = {}".format(p.get()))
    print("Member = {}".format(p.__private_member))

    p.secProp = 10
    print("List = {}".format(p.secProp))
    p.secProp = 25
    print("List = {}".format(p.secProp))
    p.secProp = 30
    print("List = {}".format(p.secProp))



