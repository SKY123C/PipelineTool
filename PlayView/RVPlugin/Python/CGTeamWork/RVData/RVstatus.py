from PySide2 import QtCore
from metaclass import singleclass
class StatusData(QtCore.QObject, metaclass=singleclass.SignalClass):
    obj = None

    def __init__(self):
        super(StatusData, self).__init__()
        self.methods = {"组长审核":"task.task_leader_status", "导演审核":"task.director_status"}
        self.examine = ['Work', 'Wait', 'Submitted', 'Check', 'Approve', 'Retake', "Fix", "Ready"]
    
    def getExamine(self):
        return self.examine
    
    def getMethods(self):
        return self.methods