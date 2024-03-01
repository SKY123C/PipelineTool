# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from PySide2 import QtCore, QtGui
from PySide2 import QtWidgets
import cgtw2
import os
import functools
from RVUtility import utilitis
from RVControllers import RVnoteGroupControll, RVretakeWidgetControll, RVsearchTControll
from metaclass import singleclass
from Widgets import RVNoteWidget, RVSearchTreeWidget


class NoteControll(QtCore.QObject, metaclass=singleclass.SignalClass):

    obj = None
    def __init__(self, noteDialog):
        self.noteDialog = noteDialog
        self.data_controll = utilitis.getControll('dataControll')
        self.tw = self.data_controll.getTW()
        self.groupControll = RVnoteGroupControll.NoteGroupControll(self.getChild([(QtWidgets.QGroupBox, 'noteInfoGroupBox')])[0])
        self.retakeControll = RVretakeWidgetControll.RetakeControll(self.getRetakeWidget())
        self.search_controll = RVsearchTControll.SearchTControll(self.getSearchDialog())
        self.__signalInit()
        super(NoteControll, self).__init__()

    def __signalInit(self):
        self.noteDialog.pushNoteBtn.clicked.connect(self.pushNote)
        self.noteDialog.imageBtn.clicked.connect(self.insertImage)
        self.noteDialog.contactBtn.clicked.connect(self.searchAccount)
        self.noteDialog.linkBtn.clicked.connect(self.link)
        self.noteDialog.noteEdit.textChanged.connect(self.addContent)
        self.noteDialog.config.connect(self.setNoteInfo)
        self.contactInit(self.search_controll.createTree)
        self.linkInit(self.search_controll.createTree)
        self.startInit()

    def clear_data(self):
        children = self.noteDialog.findChildren(RVSearchTreeWidget.ESearchDialog)
        textEdit = self.noteDialog.findChild(RVNoteWidget.NTextEdit)
        textEdit.clear()
        for child in children:
            child.close() 
        self.data_controll.clear_note_data()

    def contactInit(self, func):
        func = functools.partial(func, func1=self.searchAccount)
        self.noteDialog.contactBtn.clicked.connect(func)

    def linkInit(self, func):
        func = functools.partial(func, func1=self.link)
        self.noteDialog.linkBtn.clicked.connect(func)

    def pushNote(self):
        currentDB = self.data_controll.get_current_DB()
        module = 'shot'
        module_type = 'task'
        account = list(self.noteDialog.searchTDialog.people)
        task_id = self.data_controll.get_note_taskId()
        artist_id = self.tw.task.get(db=currentDB,
                                    module=module, id_list=task_id, 
                                    field_sign_list=['task.account_id'])[0].get('task.account_id')
        for id in account:
            if id not in artist_id:
                artist_id += ',' + id
        results = utilitis.getTextResult(self.noteDialog.noteEdit.toHtml(), self.noteDialog.noteEdit.contentList)
        info = self.isChangeStatus()
        if info.get("is_changed"):
            result = self.tw.note.create(db=currentDB, 
                                        module=module, 
                                        module_type=module_type, 
                                        link_id_list=task_id, 
                                        text=self.generateText(results),
                                        cc_account_id=artist_id)
        else:
            try:
                result = self.tw.task.update_flow(db=currentDB,
                                            module=module,  
                                            id=task_id[0],
                                            field_sign=self.data_controll.getNoteExamineMethods().get(self.groupControll.getExamine().currentText()),
                                            status=self.groupControll.getStatusBtn().currentText(),
                                            note=self.generateText(results),
                                            retake_pipeline_id_list=list(self.data_controll.get_retake_id())
                                            )
            except Exception as e:
                print(str(e))
                messageBox = QtWidgets.QMessageBox(self.noteDialog)
                messageBox.addButton(self.tr(('    Ok    ')), QtWidgets.QMessageBox.YesRole)
                if 'not in flow status' in str(e):
                    messageBox.setText(self.groupControll.getStatusBtn().currentText() + '不在审核流程状态中')
                    messageBox.exec_()
                elif 'no permission to qc' in str(e):
                    messageBox.setText('你不在审核流程中')
                    messageBox.exec_()
                result=False

        if result:
            self.noteDialog.parent().close()
            
    def insertImage(self):
        image_path = utilitis.export_current_frame()
        if os.path.exists(image_path):
            mimeData = QtCore.QMimeData()
            mimeData = QtCore.QMimeData()
            mimeData.setImageData(QtGui.QImage(image_path))
            self.noteDialog.noteEdit.insertFromMimeData(mimeData, image=image_path)
            #self.showNote([data[1]])

        # currentDB = self.data_controll.get_current_DB()
        # snipPath = self.tw.software.get_path(currentDB,'Snipaste')
        # if os.path.exists(snipPath):
        #     #self.noteDialog.setWinMinimized()
        #     time.sleep(1)
        #     cmd = '"%s" snip' % snipPath
        #     subprocess.Popen(cmd)
        #     #self.noteDialog.setWindowState(QtCore.Qt.WindowMaximized)
        # else:
        #     messageBox = QtWidgets.QMessageBox(self.noteDialog)
        #     messageBox.addButton(self.tr(('    Ok    ')), QtWidgets.QMessageBox.YesRole)
        #     messageBox.setText("请在TeamWork工具中设置正确的Snipaste路径")
        #     messageBox.exec_()
            
    def searchAccount(self):
        accountIds = self.tw.info.get_id(db='public', module='account', filter_list=[])
        self.tw.info.get(db='public', module='account', id_list=accountIds, field_sign_list=['account.name', 'account.department'])
        accountGroup = {}
        for account in self.tw.info.get(db='public', module='account', id_list=accountIds, field_sign_list=['account.name', 'account.department']):
            department = account.get('account.department')
            accountName = account.get('account.name')
            accountId = account.get('id')
            if accountGroup.get(department):
                accountGroup[department].append({'name': accountName, 'ID': accountId})
            else:
                accountGroup[department] = [{'name': accountName, 'ID': accountId}]
        
        return accountGroup
    
    def link(self):
        aniGroup = {"All": []}
        data = self.getUnderShotInfo()
        for i in data:
            aniGroup['All'].append({'name':i.get('pipeline.entity'), 'ID': i.get('task.account_id')})
        return aniGroup

    def getUnderShotInfo(self):
        currentShot = self.data_controll.get_current_shot()
        currentDB = self.data_controll.get_current_DB()
        ids = self.tw.task.get_id(db=currentDB, module='shot', filter_list=[["shot.entity","=",currentShot]])
        data = self.tw.task.get(db=currentDB, module='shot', id_list=ids, field_sign_list=['pipeline.entity', 'task.account_id', 'pipeline.id'])
        return data

    def addContent(self):
        pass
    
    def getRetakeWidget(self):
        return self.noteDialog.findChild(QtWidgets.QTableWidget, 'retakeWidget')

    def assembleContent(self, db, module, shot, stage):

        projectIds = self.tw.info.get_id('public', 'project', [['project.database', '=', db]])
        proj = self.tw.info.get('public', 'project', projectIds, ['project.entity'])
        sendID = self.tw.login.account_id()
        sendName = self.tw.info.get('public', 'account', [sendID], ['account.name'])
        str = '项目：{}\n环节: {}\n镜头号: {}\n阶段: {}\n发送人: {}'.format(proj[0].get('project.entity'), module, shot, stage, sendName[0].get('account.name'))
        return str

    def generateText(self, contentList):
        results = []
        if contentList:
            for content in contentList:
                if os.path.exists(content):
                    results.append({'type': 'image', 'path': content})
                else:
                    results.append({'type': 'text', 'content': content})
        
        return results

    def getChild(self, objectList):
        obj = []
        for classType, name in objectList:
            obj.append(self.noteDialog.findChild(classType, name))
        return obj

    def getSearchDialog(self):
        return self.noteDialog.searchTDialog
    
    def getAllInfo(self):
        project, fileInfo, creaters, examine, btn= self.getChild([(QtWidgets.QLabel, 'noteProject'), 
                        (QtWidgets.QLabel, 'noteFileInfo'), 
                        (QtWidgets.QLabel, 'noteCreaters'), 
                        (QtWidgets.QComboBox, 'statusCombox'),
                        (QtWidgets.QComboBox, 'examineMethods')])

        return [project, fileInfo, creaters, examine, btn]

    def startInit(self):
        combox = self.getChild([(QtWidgets.QComboBox, 'statusCombox')])[0]
        combox.addItems(self.data_controll.getProjectExamine())
        btn = self.getChild([(QtWidgets.QComboBox, 'examineMethods')])[0]
        btn.addItems(self.data_controll.getNoteExamineMethods().keys())
    
    def setNoteInfo(self):
        note_data = self.data_controll.get_note_data_info()
        print(".................")
        print(note_data)
        if note_data:
            self.setLabelComboBox([os.path.join(note_data.get('shot'), note_data.get('stage')), note_data.get('author'), note_data.get('leader_status'), note_data.get('projectName')])
            self.retakeControll.addItem(self.getUnderShotInfo())
            self.noteDialog.show()

    
    def setLabelComboBox(self, info):
        projectLabel, fileLabel, creatersLabel, examine, statusLabel = self.getAllInfo()
        fileLabel.setText(info[0])
        creatersLabel.setText(info[1])
        examine.setCurrentIndex(self.data_controll.getProjectExamine().index(info[2]))
        projectLabel.setText(info[3])
    
    def isChangeStatus(self):
        Noteinfo = self.data_controll.get_note_data_info()
        currentStatus = self.groupControll.getStatusBtn().currentText()
        return {"current_status": currentStatus, "is_changed": currentStatus == Noteinfo.get('leader_status')}
    
    def init(self):
        self.clear_data()
        self.data_controll.set_note_data_info()
        self.setNoteInfo()