
from PySide6 import QtCore
from rvcore.base_classes import singleclass


class Manager(QtCore.QObject, metaclass=singleclass.SignalClass):


    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def get_instance(cls):
        return cls.instance