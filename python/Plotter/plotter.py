
import imp
import typing
from os.path import abspath, dirname, join
from Backend.backend import Backend
from Logger import logger
from PySide2.QtWidgets import QApplication
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtCore import QObject, Slot, Signal




class  Plotter(QObject):
    
    def __init__(self, args, config: typing.Dict) -> None:
        super().__init__()
        
        self.__app = QApplication(args)
        self.__engine = QQmlApplicationEngine()

        self.setImportPaths(config["imports"])
        # Expose the Python object to QML
        self.__context = self.__engine.rootContext()
        # Get the path of the current directory, and then add the name
        # of the QML file, to load it.
        self.__qmlFile = join(dirname(__file__), '../../qml/main.qml')

        self.__backend = None
    
    def set_backend(self, backend: Backend):        
        self.__backend = backend
        self.__context.setContextProperty("Backend", backend)

    def load_app(self):
        self.__engine.load(abspath(self.__qmlFile))
        self.__backend.setupUi(self.__backend.ui_config)

    def run(self) -> int: 
        return self.__app.exec_()

    def rootObjects(self) -> typing.List:
        return self.__engine.rootObjects() 

    def setImportPaths(self, path_lst: typing.List):
        importlst = self.__engine.importPathList()
        for path in path_lst:
            importlst.append(join(dirname(__file__),path))
        self.__engine.setImportPathList(importlst)
   
    def setup(self, config: dict):
        pass
