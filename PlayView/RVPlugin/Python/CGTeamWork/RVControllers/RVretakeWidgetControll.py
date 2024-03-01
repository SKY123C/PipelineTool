# -*- coding: utf-8 -*-
from PySide2 import QtWidgets,QtCore
from RVUtility import utilitis
from metaclass import singleclass


class RetakeControll(QtCore.QObject, metaclass=singleclass.SignalClass):

    obj=None
    def __init__(self, widget):
        self.retakeWidget = widget
        self.data_controll = utilitis.getControll('dataControll')
        super(RetakeControll, self).__init__()
        self._signalInit()

    def _signalInit(self):
        
        self.retakeWidget.cellChanged.connect(self.setRetakeItem)
    
    def setRetakeItem(self, row, column):
        item = self.retakeWidget.item(row, column)
        if item.checkState():
            self.data_controll.add_retake_id(item.pipelineId)

    def addItem(self, data):
        self.retakeWidget.clear()
        data = [i for i in data if i.get('pipeline.entity') != self.data_controll.get_current_stage()]
        row = int(len(data)/4 +1)
        self.retakeWidget.setRowCount(row)
        self.retakeWidget.setColumnCount(4)
        c = [data[i:i+4] for i in range(0, len(data), 4)]
        for index, value in enumerate(c):
            for index1, value1 in enumerate(value):
                item = QtWidgets.QTableWidgetItem(value1.get('pipeline.entity'))
                item.setCheckState(QtCore.Qt.Unchecked)
                item.pipelineId = value1.get('pipeline.id')
                self.retakeWidget.setItem(index, index1, item)
