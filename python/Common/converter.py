from PySide2.QtQml import QJSValue



class Converter(): 
    def __init__(self) -> None:
        pass
    

    @staticmethod
    def list_to_jsvalue(data_list):
        value = QJSValue()
        for i in range(len(data_list)):
            if(type(data_list[i]) == dict):
                sub_value = Converter.dict_to_jsvalue(data_list[i])
                value.setProperty(i,sub_value)   
            elif type(data_list[i]) == list:
                sub_value = Converter.list_to_jsvalue(data_list[i])
                value.setProperty(i,sub_value)
            else:
                value.setProperty(i,data_list[i])
        return value

    @staticmethod
    def dict_to_jsvalue(data_dict):
        value = QJSValue()
        for (k,v) in data_dict.items():
            if(type(v) == dict):
                sub_value = Converter.dict_to_jsvalue(v)
                value.setProperty(k,sub_value)   
            elif type(v) == list:
                sub_value = Converter.list_to_jsvalue(v)
                value.setProperty(k,sub_value)
            else:
                value.setProperty(k,v)
        return value
    

        print("Key = {} | Value = {} | Type = {}".format(k,v, type(v)))
        


    @staticmethod
    def jsvalue_to_dict(jsvalue):
        pass