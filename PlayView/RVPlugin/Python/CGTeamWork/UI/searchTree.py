# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'searchTreetyFDbJ.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_TreeDialog(object):
    def setupUi(self, TreeDialog):
        if not TreeDialog.objectName():
            TreeDialog.setObjectName(u"TreeDialog")
        TreeDialog.resize(413, 332)
        self.verticalLayout_2 = QVBoxLayout(TreeDialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(TreeDialog)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout_2 = QHBoxLayout(self.widget)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.searchBtn = QPushButton(self.widget)
        self.searchBtn.setObjectName(u"searchBtn")

        self.horizontalLayout.addWidget(self.searchBtn)

        self.nameInputBtn = QLineEdit(self.widget)
        self.nameInputBtn.setObjectName(u"nameInputBtn")

        self.horizontalLayout.addWidget(self.nameInputBtn)


        self.horizontalLayout_2.addLayout(self.horizontalLayout)


        self.verticalLayout.addWidget(self.widget)

        self.treeFillter = QTreeWidget(TreeDialog)
        self.treeFillter.setHeaderHidden(True)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.treeFillter.setHeaderItem(__qtreewidgetitem)
        self.treeFillter.setObjectName(u"treeFillter")

        self.verticalLayout.addWidget(self.treeFillter)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.confirmBtn = QPushButton(TreeDialog)
        self.confirmBtn.setObjectName(u"confirmBtn")
        self.confirmBtn.setMinimumSize(QSize(0, 30))
        self.horizontalLayout_3.addWidget(self.confirmBtn)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(TreeDialog)

        QMetaObject.connectSlotsByName(TreeDialog)
    # setupUi

    def retranslateUi(self, TreeDialog):
        TreeDialog.setWindowTitle(QCoreApplication.translate("TreeDialog", "Dialog", None))
        self.searchBtn.setText("")
        self.nameInputBtn.setText("")
        self.confirmBtn.setText(QCoreApplication.translate("TreeDialog", "确定", None))
    # retranslateUi

