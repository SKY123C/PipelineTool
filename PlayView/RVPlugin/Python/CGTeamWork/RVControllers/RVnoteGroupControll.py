from PySide2 import QtWidgets, QtCore
from metaclass import singleclass


class NoteGroupControll(QtCore.QObject, metaclass=singleclass.SignalClass):

    obj = None
    def __init__(self, group):
        self.groupBox = group
        super(NoteGroupControll, self).__init__()
        self._signalInit()

    def getStatusBtn(self):
        btn = self.groupBox.findChild(QtWidgets.QComboBox, 'statusCombox')
        return btn

    def getExamine(self):
        return self.groupBox.findChild(QtWidgets.QComboBox, 'examineMethods')

    def _signalInit(self):
        pass


