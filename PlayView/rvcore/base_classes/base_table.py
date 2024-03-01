from typing import Optional
from PySide6 import QtWidgets, QtGui, QtCore
from enum import Enum

class TableType(Enum):
    TABLE = 0
    GLOBALTABLE = 1
    
class ShotInfo:
    
    def __init__(self, shot_count, **kwargs) -> None:
        self.__data = {}
        self.__data["镜头数量"] = shot_count
        self.parse(kwargs)
    
    def parse(self, data_dict):
        for key, value_dict in data_dict.items():
            for label, value in value_dict.items():
                self.__data[label] = value
    
    def get_data(self):
        return self.__data
            
    
class RVTable(QtWidgets.QTableView):
    
    resized = QtCore.Signal(QtCore.QSize)
    
    def __init__(self, table_type, parent=None) -> None:
        super().__init__(parent)
        self.__table_type = table_type
    
    def get_table_type(self):
        return self.__table_type
    
    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        self.resized.emit(QtCore.QSize(self.width(), self.height()))
        return super().resizeEvent(event)