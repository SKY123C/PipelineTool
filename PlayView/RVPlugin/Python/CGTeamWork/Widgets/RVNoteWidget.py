from UI import NoteUI
from PySide2 import QtCore, QtWidgets, QtGui

import os
import time
from UI import NoteUI
from Widgets import RVSearchTreeWidget
from RVUtility import utilitis
import rv.qtutils


class ENoteDialog(QtWidgets.QWidget, NoteUI.Ui_Dialog):
    
    config = QtCore.Signal()
    def __init__(self, parent=None):
        super(ENoteDialog, self).__init__(parent=parent)
        self.setObjectName("NoteDialog")
        self.setupUi(self)
        self.setIcon()
        self.searchTDialog = RVSearchTreeWidget.ESearchDialog(self)
        self.rvMediaName = None
        self.isStatusChanged = False
        self.setWindowFlags(QtCore.Qt.Tool|QtCore.Qt.Widget)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle('Push Note')

    def moveEvent(self, event):
        children = self.findChildren(RVSearchTreeWidget.ESearchDialog)
        for child in children:
            relPos = event.pos() - event.oldPos()
            child.move(child.pos()+ relPos)
    
    def showEvent(self, event):
        utilitis.setWidgetSize(self, 0.26, 0.64)
        self.move(*utilitis.getMousePos())
        return super().showEvent(event)

    def setIcon(self):
        path = os.path.dirname(os.path.dirname(__file__))
        self.imageBtn.setIcon(QtGui.QIcon(os.path.join(path, 'Resources/Icons', 'screenshot.svg')))
        self.contactBtn.setIcon(QtGui.QIcon(os.path.join(path, 'Resources/Icons', 'contact.svg')))
        self.linkBtn.setIcon(QtGui.QIcon(os.path.join(path, 'Resources/Icons', 'link.svg')))
    
    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            pos = event.globalPos()
            if self.childAt(pos) != self.searchTDialog:
                self.searchTDialog.close()

    def getStatusChanged(self):
        return self.isStatusChanged

class NTextEdit(QtWidgets.QTextEdit):
    
    def __init__(self, parent=None):
        self.imagePath = []
        super(NTextEdit, self).__init__(parent=parent)
        self.setFont(QtGui.QFont("Microsoft YaHei", 20))
        self.contentList = []
        self.netImage = ''

    def insertFromMimeData(self, miniData, image=None):

        if miniData.hasImage():
            self.addImage(miniData.imageData(), image)
        elif miniData.hasText():
            self.contentList.append(miniData.text())
            super(NTextEdit, self).insertFromMimeData(miniData)

    def addImage(self, varientData, image=None):
        byteArray = QtCore.QByteArray()
        buffer = QtCore.QBuffer(byteArray)
        if image:
            savePath = image
        else:
            savePath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Resources/save/', str(time.time()) + '.jpg')
            varientData.save(savePath, 'jpg')
        if os.path.exists(savePath):
            self.imagePath.append(savePath)
            self.contentList.append(savePath)
            imageData = varientData.scaled(175, 129)
            imageData.save(buffer, 'jpg')
            base64Data = str(byteArray.toBase64())[2:-1]
            richText = '<img src="data:image/jpg;base64,{}">'.format(base64Data)
            fragement = QtGui.QTextDocumentFragment.fromHtml(richText)
            self.textCursor().insertFragment(fragement)

    def clear(self):
        utilitis.deleteFiles(self.contentList)
        self.contentList = []
        super(NTextEdit, self).clear()

    def mousePressEvent(self, event):
        
        if event.button() == QtCore.Qt.LeftButton:
            self.parent().parentWidget().searchTDialog.close()
    
    def setNetImage(self, path):
        self.netImage = path
    

class NGroupBox(QtWidgets.QGroupBox):
    def __init__(self, parent):
        super(NGroupBox,self).__init__(parent=parent)


class NComboBox(QtWidgets.QComboBox):
    def __init__(self, parent):
        super(NComboBox, self).__init__(parent=parent)
        self.setView(QtWidgets.QListView())
