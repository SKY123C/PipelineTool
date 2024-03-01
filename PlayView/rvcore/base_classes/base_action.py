
from PySide6 import QtWidgets, QtGui
import enum
from rvcore import utl

class MenuType(enum.Enum):
    TABLE = 1
    

class RVAction(QtGui.QAction):
    menu_type = []
    active = True
    def __init__(self, action_name, **kwargs) -> None:
        super().__init__(action_name)
        self.triggered.connect(self.action_callback)
        self.interface = utl.TWLib()
    
    def action_callback(self, *args):
        ...
    
    def set_icon(self):
        ...
    
    def rule(self):
        return True

class TableAction(RVAction):
    menu_type = [MenuType.TABLE]
    active = False
    def __init__(self, action_name, **kwargs) -> None:
        super().__init__(action_name, **kwargs)
        self.__index_list = kwargs.get("index_list")
        self.table: QtWidgets.QTableView = kwargs.get("table")
        
    def get_model_index_List(self):
        return self.__index_list