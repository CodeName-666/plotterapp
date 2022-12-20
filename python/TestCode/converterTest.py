
from Common.converter import Converter

from PySide6.QtQml import QJSValue





if __name__ == "__main__":
    
    l = {}
    l["A"] = 10
    l["B"] = 20
    l["C"] = 30
    l["E"] = ['TEST1','TEST2','TEST3']
    l["D"] = {'color': 'blue', 'fruit': 'apple', 'pet': 'dog'}

    x = Converter.dict_to_jsvalue(l)

    for (k,v) in l.items(): 
        print("Key = {} | Value = {} | Type = {}".format(k,v, type(v)))
        if type(v) == dict:
            print("Is Dict")
        if type(v) == list:
            x = QJSValue()
            for i in range(len(v)):
                x.setProperty(i,v[i])
                
    
   