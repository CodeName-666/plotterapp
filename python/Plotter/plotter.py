
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
        
        self._app = QApplication(args)
        self._engine = QQmlApplicationEngine()

        self.setImportPaths(config["imports"])
        # Expose the Python object to QML
        self._context = self._engine.rootContext()
        # Get the path of the current directory, and then add the name
        # of the QML file, to load it.
        self._qmlFile = join(dirname(__file__), '../../qml/main.qml')

        self._backend = None
    
    def set_backend(self, backend: Backend):        
        self._backend = backend
        self._context.setContextProperty("Backend", backend)

    def load_app(self):
        self._engine.load(abspath(self._qmlFile))

    def run(self) -> int: 
        self._backend.new_graph.emit("test",None)
        return self._app.exec_()

    def rootObjects(self) -> typing.List:
        return self._engine.rootObjects() 

    def setImportPaths(self, path_lst: typing.List):
        importlst = self._engine.importPathList()
        for path in path_lst:
            importlst.append(join(dirname(__file__),path))
        self._engine.setImportPathList(importlst)
   
    def setup(self, config: dict):
        pass
