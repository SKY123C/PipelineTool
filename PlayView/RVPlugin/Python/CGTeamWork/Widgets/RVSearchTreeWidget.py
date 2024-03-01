# -*- coding: utf-8 -*-
from PySide2 import QtWidgets, QtCore, QtGui
from UI import searchTree
from RVUtility import utilitis


class ESearchDialog(QtWidgets.QDialog, searchTree.Ui_TreeDialog):

    def __init__(self, parent=None):

        super(ESearchDialog, self).__init__(parent=parent)
        self.people = set()
        self.setupUi(self)
        #self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.Dialog|QtCore.Qt.FramelessWindowHint)
        #self.setStyleSheet(utilitis.readQSS('search.qss'))
        utilitis.setWidgetSize(self, 0.11, 0.28)

    def showEvent(self, event):
        parent = self.parentWidget()
        if parent:
            mousePos = utilitis.getMousePos()
            self.move(mousePos[0], mousePos[1])

    # def paintEvent(self, event):
    #     path = QtGui.QPainterPath()
    #     path.setFillRule(QtCore.Qt.WindingFill)
    #     pat = QtGui.QPainter(self)
    #     pat.setRenderHint(pat.Antialiasing)
    #     pat.fillPath(path, QtGui.QBrush(QtCore.Qt.white))
    #     color = QtGui.QColor(192, 192, 192, 50)
    #     for i in range(10):
    #         i_path = QtGui.QPainterPath()
    #         i_path.setFillRule(QtCore.Qt.WindingFill)
    #         ref = QtCore.QRectF(10-i, 10-i, self.width()-(10-i)*2, self.height()-(10-i)*2)
    #         # i_path.addRect(ref)
    #         i_path.addRoundedRect(ref, 10, 10)
    #         color.setAlpha(150 - i**0.5*50)
    #         pat.setPen(color)
    #         pat.drawPath(i_path)
    #     pat2 = QtGui.QPainter(self)
    #     pat2.setRenderHint(pat2.Antialiasing) 
    #     pat2.setBrush(QtCore.Qt.white)
    #     pat2.setPen(QtCore.Qt.transparent)
    #     rect = self.rect()
    #     rect.setLeft(9)
    #     rect.setTop(9)
    #     rect.setWidth(rect.width()-9)
    #     rect.setHeight(rect.height()-9)
    #     pat2.drawRoundedRect(rect, 4, 4)
        