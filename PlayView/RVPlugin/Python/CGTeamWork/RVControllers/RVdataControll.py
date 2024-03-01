
from PySide2 import QtCore
from metaclass import singleclass
from RVData import RVproject, RVnote, RVstatus
import cgtw2
import os
from rv import commands as rvc
import json
from RVUtility import utilitis

class DataList(QtCore.QObject, metaclass=singleclass.SignalClass):
    obj = None
    def __init__(self):
        self.tw = cgtw2.tw()
        self.projectData = RVproject.ProjectData(self.tw)
        self.statusData = RVstatus.StatusData()
        self.noteData = RVnote.NoteData()
        self.projectName = ''
        self.configPath = os.path.join(utilitis.create_temp_dir('images'), 'preset.json')
        self.imagesPath = utilitis.create_temp_dir('images')

    def addListItem(self, listWidget):
        projects = self.getProjectMap().keys()
        listWidget.addItems(list(projects))

    def getProjectMap(self):
        return self.projectData.DBMap

    def setCurrentDB(self, text):
        currentDB = self.projectData.setDB(text)
        self.projectName = text
        return currentDB

    def getCurrentDB(self):
        return self.projectData.getDB()

    def getOutPath(self):
        return self.projectData.specialPath

    def get_note_taskId(self):
        return [self.noteData.currnet_taskId]

    def getProjectExamine(self):
        return self.statusData.getExamine()
    
    def getNoteExamineMethods(self):
        return self.statusData.getMethods()
    
    def set_note_data_info(self):
        value_dict = self.get_current_frame_data()
        self.noteData.setData(value_dict)
    
    def get_current_frame_data(self):
        current_frame = rvc.frame()
        current_sources = rvc.sourcesAtFrame(current_frame)
        if current_sources:
            value_dict = json.loads(os.environ.get("TEAMWORKINFO"))
            for key in value_dict:
                value = rvc.getStringProperty(current_sources[0] + f".attributes.comment_{key}")[0]
                value_dict[key] = value
            return value_dict

    def getCurrentProjectName(self):
        return self.projectData.getProjectName()
    
    def getProjectData(self):
        return self.projectData
    
    def getAllStatus(self):
        return self.projectData.getAllStatus()
    
    def getTW(self):
        return self.tw
    
    def getConfigPath(self):
        return self.configPath
    
    def get_note_data_info(self):
        return self.noteData.getData()
    
    def add_retake_id(self, id):
        self.noteData.addRetakeID(id)
    
    def get_current_stage(self):
        return self.noteData.current_stage
    
    def get_current_shot(self):
        return self.noteData.current_shot
    
    def get_current_DB(self):
        return self.noteData.current_DB
    
    def clear_note_data(self):
        self.noteData.clearData()
    
    def get_retake_id(self):
        return self.noteData.current_retakeID