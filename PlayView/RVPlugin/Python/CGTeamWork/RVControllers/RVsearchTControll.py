# -*- coding: utf-8 -*-
from PySide2 import QtCore
from PySide2 import QtWidgets, QtGui
from RVUtility import utilitis
import os
from metaclass import singleclass


class SearchTControll(QtCore.QObject, metaclass=singleclass.SignalClass):

    obj=None
    def __init__(self, searchTreeDialog):
        self.searchTreeDialog = searchTreeDialog
        super(SearchTControll, self).__init__()
        self.__signalInit()
        self.widgetInit()

    def widgetInit(self):
        self.searchTreeDialog.searchBtn.setIcon(QtGui.QIcon(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Resources/icons/', 'search.svg')))
    
    def __signalInit(self):
        self.searchTreeDialog.treeFillter.itemChanged.connect(self.selectChild)
        self.searchTreeDialog.confirmBtn.clicked.connect(self.confirmPeople)
        self.searchTreeDialog.treeFillter.itemClicked.connect(self.addPeople)
        self.searchTreeDialog.searchBtn.clicked.connect(self.search)

    def createTree(self, func1):
        self.searchTreeDialog.treeFillter.clear()
        treeData = func1()
        self.searchTreeDialog.treeFillter.setColumnCount(1)
        for deparment, item in treeData.items():
            rootNode = QtWidgets.QTreeWidgetItem(self.searchTreeDialog.treeFillter)
            rootNode.setCheckState(0, QtCore.Qt.Unchecked)
            rootNode.setText(0, deparment)
            for data in item:
                name, id = data.items()
                child = QtWidgets.QTreeWidgetItem(rootNode)
                child.setText(0, name[1])
                child.setCheckState(0, QtCore.Qt.Unchecked)
                child.id = id[1]
        self.searchTreeDialog.show()
    
    def selectChild(self, item, column):
        count = item.childCount()
        if count:
            checkState = item.checkState(0)
            for i in range(0,count):
                item.child(i).setCheckState(0, checkState)

    def confirmPeople(self):

        self.searchTreeDialog.close()
        
    def addPeople(self, item, column):
        isexitsChild = item.childCount()
        if isexitsChild:
            for i in range(0, isexitsChild):
                childItem = item.child(i)
                if childItem.checkState(column):
                    idTuple = childItem.id.split(',')
                    self.searchTreeDialog.people.update(idTuple)
                else:
                    for i in childItem.id.split(','):
                        self.searchTreeDialog.people.discard(i)
        else:
            if item.checkState(column):
                idTuple = item.id.split(',')
                self.searchTreeDialog.people.update(idTuple)
            else:
                for i in item.id.split(','):
                    self.searchTreeDialog.people.discard(i)

    def search(self):

        for parent_index in range(self.searchTreeDialog.treeFillter.topLevelItemCount()):
                self.searchTreeDialog.treeFillter.topLevelItem(parent_index).setExpanded(False)
        text = self.searchTreeDialog.nameInputBtn.text()
        items = self.searchTreeDialog.treeFillter.findItems(text, QtCore.Qt.MatchContains|QtCore.Qt.MatchRecursive)

        if items:
            for item in items:
                parent = item.parent()
                if parent:
                    parent.setExpanded(True)
            
            self.searchTreeDialog.treeFillter.setCurrentItem(item)