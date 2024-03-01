from PySide2 import QtCore
from metaclass import singleclass
class ProjectData(QtCore.QObject, metaclass=singleclass.SignalClass):
    obj = None
    
    def __init__(self, tw):
        
        self.tw = tw
        self.currentData = None
        self.projectName = ''
        self.currentAni = None
        self.anis = None
        self.specialPath = r"\\10.236.200.22\VEoutput"
        self.extralLabels = ['最新修改环节', '镜头进行到的最后环节']
        self.allStages = ['LAY', 'ANI', 'CFX', 'EFX', 'SET', 'LGT', 'CMP', 'RCL', 'PKG']
        self.horizontalLabels = []
        self.color = {"Check": [243, 208, 0], "Approve": [0, 172, 86], "Submitted": [0, 255, 0], "Work": [88, 112, 254], "Retake":[255, 62, 62], 'Wait': [90, 91, 93], 'Fix':[254, 21, 121], 'Ready': [134, 14, 254], 'Close': [75, 75, 75], 'Pause':[255, 158, 62]}
        self.status = ['Work', 'Retake', 'Approve', 'Check', 'Pause', 'Wait', "Fix", "Ready", "Close", "Submitted"]
        self.horizontalLabels.extend(self.allStages)
        self.horizontalLabels.extend(self.extralLabels)
        self._DBInit()
    
    def _DBInit(self):
        self.DBMap = {}
        id_list =  self.tw.info.get_id(db='public', module='project', filter_list=[['project.status','=','Active']])
        for i in self.tw.info.get(db='public', module='project', id_list=id_list, field_sign_list=['project.entity','project.database']):
            self.DBMap[i.get('project.entity')] = i.get('project.database')

    def setDB(self, text):
        db = self.DBMap.get(text)
        if db:
            self.currentData = db
            self.projectName = text
        return self.currentData

    def getDB(self):
        return self.currentData
    
    def getOutPath(self):
        return self.specialPath
    
    def getProjectName(self):
        return self.projectName
    
    def getColor(self):
        return self.color
    
    def getAllStatus(self):
        return self.status
    
    def getHorizontalLabels(self):
        return self.horizontalLabels
    
    def getTw(self):
        return self.tw
    
    def getStages(self):
        return self.allStages
    
    def getAni(self):
        return self.currentAni
    
    def setAni(self, ani):
        self.currentAni = ani
    
    def getAllAnis(self):
        return self.anis
    
    def setAllAnis(self, anis):
        self.anis = anis
    
    def getSpecialStage(self):
        return ['rcl', 'cmp', 'pkg']
    
