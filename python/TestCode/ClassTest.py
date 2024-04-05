

class TestClass:


    def __init__(self, value1, value2) -> None:
        print("NONE Params")

    def __init__(self, value) -> None:
        print("With Params: {}".format(value))

if __name__ == "__main__":
    
    t = TestClass(10,29)
    p = TestClass(50)