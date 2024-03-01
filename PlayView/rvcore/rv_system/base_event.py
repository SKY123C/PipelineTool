from PySide6 import QtCore, QtWidgets, QtGui
from typing import *
import traceback


'''
适用于全局事件
1.注册事件
2.收集事件
3.事件回调
'''
class RVEvent(QtCore.QObject):
    rv_event = QtCore.Signal(dict)
    def __init__(self, parent=None, event_name:str=None) -> None:
        super().__init__(parent=parent)
        self.__event_name = event_name if event_name else self.__class__.__name__
        self.__func_list = []
        self.rv_event.connect(self.start)

    @property
    def event_name(self):
        return self.__event_name
    
    def add_func(self, func, *args):
        self.__func_list.append(func)
        self.__func_list.extend(args)

    
    def start(self, data):
        for func in self.__func_list:
            if hasattr(func, "__call__"):
                try:
                    func(data)
                except Exception as e:
                    print(traceback.format_exc())


class RVInitEvent(RVEvent):

    def __init__(self, parent=None, event_name:str=None) -> None:
        super().__init__(parent=parent, event_name=event_name)


class DataLoadFinshed(RVEvent):

    def __init__(self, parent=None, event_name:str=None) -> None:
        super().__init__(parent=parent, event_name=event_name)


class AniChangeEvent(RVEvent):
    def __init__(self, parent=None, event_name:str=None) -> None:
        super().__init__(parent=parent, event_name=event_name)


class ProjectChangeEvent(RVEvent):
    def __init__(self, parent=None, event_name:str=None) -> None:
        super().__init__(parent=parent, event_name=event_name)


class TableItemFinished(RVEvent):
    def __init__(self, parent=None, event_name:str=None) -> None:
        super().__init__(parent=parent, event_name=event_name)


class TabIndexChangeEvent(RVEvent):
    def __init__(self, parent=None, event_name:str=None) -> None:
        super().__init__(parent=parent, event_name=event_name)


class TabDeleteEvent(RVEvent):
    def __init__(self, parent=None, event_name:str=None) -> None:
        super().__init__(parent=parent, event_name=event_name)

class ProjectSaveStateChangeEvent(RVEvent):
    def __init__(self, parent=None, event_name:str=None) -> None:
        super().__init__(parent=parent, event_name=event_name)

class SessionSaveStateChangeEvent(RVEvent):
    def __init__(self, parent=None, event_name:str=None) -> None:
        super().__init__(parent=parent, event_name=event_name)
        

class FavoriteClickedEvent(RVEvent):
    def __init__(self, parent=None, event_name:str=None) -> None:
        super().__init__(parent=parent, event_name=event_name)
        

class InitFinishedEvent(RVEvent):
    def __init__(self, parent=None, event_name:str=None) -> None:
        super().__init__(parent=parent, event_name=event_name)