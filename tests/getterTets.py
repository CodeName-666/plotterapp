


class Test():

    def __init__(self) -> None:
        self._x = 0

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, nX):
        self._x = nX



if __name__ == "__main__":

    t = Test()
    print("t.x = {}".format(t.x))
