from PySide2.QtCore import QObject, Slot, Signal, QTimer, Property

class D():
    alpa = Signal()
    blubb_works_good = Signal(bool)
    
    def __init__(self) -> None:
        self.blubb_works_good.connect(self.test)
        self.blubb_works_good.emit(True)
    

    def test(self, status):
        print("TEST SLOT {}".format(status))



class C():
    signal = Signal()
    statusChanged = Signal(bool)

    def __init__(self) -> None:
        self.signal.connect(self.cbk)
        self.statusChanged.connect(self.status_cbk)
        self.signal.emit()
        self.status = True
    
    @Property(bool, notify=statusChanged)
    def status(self) ->bool:
        try:
            return self.__status
        except:
            return False

    @status.setter
    def status(self, nStatus:bool):
        if self.status != nStatus:
            self.__status = nStatus
            self.statusChanged.emit(nStatus)

    def status_cbk(self, status:bool):
        print("Status =  {}".format(status))

    def cbk(self):
        print("Works")


class B(QObject):
    def __init__(self) -> None:
        QObject.__init__(self)


class A(C,B,D):
    def __init__(self) -> None:
        B.__init__(self)
        C.__init__(self)
        D.__init__(self)


class Test(QObject):
    sig = Signal()
    statusChanged = Signal()

    def __init__(self) -> None:
        super(Test,self).__init__()
        self.__private_member = 10
        #self.sig.connect(self.cbk)
        self.statusChanged.connect(self.cbk)


    @Property(bool,notify=statusChanged)
    def status(self) -> bool:
        try:
            return self._status
        except:
            return False

    @status.setter
    def status(self, status):
        if self.status != status:
            self._status = status
            self.statusChanged.emit()


    def cbk(self):
        print("Works")

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

def firstTest(): 
    p = Test()
    
    p.status = True

    p.testProp = 5
    b = p.testProp
    print("Member = {}".format(p.get()))
    p.secProp = 10
    print("List = {}".format(p.secProp))
    p.secProp = 25
    print("List = {}".format(p.secProp))
    p.secProp = 30
    print("List = {}".format(p.secProp))

if __name__ == "__main__":
    var = A()



