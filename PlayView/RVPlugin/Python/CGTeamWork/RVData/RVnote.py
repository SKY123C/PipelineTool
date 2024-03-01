from PySide2 import QtCore
from metaclass import singleclass
class NoteData(QtCore.QObject, metaclass=singleclass.SignalClass):
    obj = None
    
    def __init__(self):
        super(NoteData, self).__init__()
        self.data = {}
        self.retakeID = set()
    
    def setData(self, value_dict):
        print("************")
        print(value_dict)
        self.data = value_dict
    
    def getData(self):
        #data = {'taskId': self.currentID, 'currentShot': self.currentShot, 'currentStage': self.currentStage, 'producer':self.producer, 'status': self.status}
        return self.data

    @property
    def current_stage(self):
        return self.data.get("stage")

    @property
    def currnet_taskId(self):
        return self.data.get("taskId")
    
    @property
    def current_shot(self):
        return self.data.get("shot")
    
    @property
    def current_author(self):
        return self.data.get("author")
    
    @property
    def current_DB(self):
        return self.data.get("projectDB")
    
    @property
    def current_retakeID(self):
        return list(self.retakeID)

    def clearData(self):
        self.data.clear()
        self.retakeID = set()
    
    def addRetakeID(self, id):
        self.retakeID.add(id)
