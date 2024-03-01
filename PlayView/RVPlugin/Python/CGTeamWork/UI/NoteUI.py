# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'noteRJeurf.ui'
##
## Created by: Qt User Interface Compiler version 5.15.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


from Widgets import RVNoteWidget


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(521, 659)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(100, 200))
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(Dialog)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_4 = QVBoxLayout(self.widget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.noteInfoGroupBox = RVNoteWidget.NGroupBox(self.widget)
        self.noteInfoGroupBox.setObjectName(u"noteInfoGroupBox")
        self.noteInfoGroupBox.setMinimumSize(QSize(0, 0))
        self.noteInfoGroupBox.setFlat(False)
        self.verticalLayout_13 = QVBoxLayout(self.noteInfoGroupBox)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_12 = QVBoxLayout()
        self.verticalLayout_12.setSpacing(6)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setLabelAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.formLayout.setVerticalSpacing(15)
        self.label = QLabel(self.noteInfoGroupBox)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.noteProject = QLabel(self.noteInfoGroupBox)
        self.noteProject.setObjectName(u"noteProject")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.noteProject)

        self.label_3 = QLabel(self.noteInfoGroupBox)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_3)

        self.noteFileInfo = QLabel(self.noteInfoGroupBox)
        self.noteFileInfo.setObjectName(u"noteFileInfo")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.noteFileInfo)

        self.label_5 = QLabel(self.noteInfoGroupBox)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_5)

        self.noteCreaters = QLabel(self.noteInfoGroupBox)
        self.noteCreaters.setObjectName(u"noteCreaters")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.noteCreaters)

        self.label_7 = QLabel(self.noteInfoGroupBox)
        self.label_7.setObjectName(u"label_7")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_7)

        self.statusCombox = RVNoteWidget.NComboBox(self.noteInfoGroupBox)
        self.statusCombox.setObjectName(u"statusCombox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.statusCombox.sizePolicy().hasHeightForWidth())
        self.statusCombox.setSizePolicy(sizePolicy1)
        self.statusCombox.setMinimumSize(QSize(80, 0))

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.statusCombox)

        self.label_2 = QLabel(self.noteInfoGroupBox)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_2)

        self.examineMethods = RVNoteWidget.NComboBox(self.noteInfoGroupBox)
        self.examineMethods.setObjectName(u"examineMethods")
        sizePolicy1.setHeightForWidth(self.examineMethods.sizePolicy().hasHeightForWidth())
        self.examineMethods.setSizePolicy(sizePolicy1)
        self.examineMethods.setMinimumSize(QSize(75, 0))

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.examineMethods)


        self.verticalLayout_12.addLayout(self.formLayout)


        self.verticalLayout_13.addLayout(self.verticalLayout_12)


        self.verticalLayout_3.addWidget(self.noteInfoGroupBox)

        self.line = QFrame(self.widget)
        self.line.setObjectName(u"line")
        self.line.setFrameShadow(QFrame.Raised)
        self.line.setFrameShape(QFrame.HLine)

        self.verticalLayout_3.addWidget(self.line)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_3.addWidget(self.label_4)

        self.retakeWidget = QTableWidget(self.widget)
        self.retakeWidget.setObjectName(u"retakeWidget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.retakeWidget.sizePolicy().hasHeightForWidth())
        self.retakeWidget.setSizePolicy(sizePolicy2)
        self.retakeWidget.setFocusPolicy(Qt.NoFocus)
        self.retakeWidget.setFrameShape(QFrame.NoFrame)
        self.retakeWidget.setFrameShadow(QFrame.Sunken)
        self.retakeWidget.setLineWidth(0)
        self.retakeWidget.setAutoScrollMargin(16)
        self.retakeWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.retakeWidget.setTabKeyNavigation(False)
        self.retakeWidget.setProperty("showDropIndicator", False)
        self.retakeWidget.setSelectionMode(QAbstractItemView.NoSelection)
        self.retakeWidget.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.retakeWidget.setTextElideMode(Qt.ElideNone)
        self.retakeWidget.setShowGrid(False)
        self.retakeWidget.setGridStyle(Qt.NoPen)
        self.retakeWidget.setWordWrap(False)
        self.retakeWidget.setCornerButtonEnabled(False)
        self.retakeWidget.horizontalHeader().setVisible(False)
        self.retakeWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.retakeWidget.horizontalHeader().setHighlightSections(True)
        self.retakeWidget.verticalHeader().setVisible(False)
        self.retakeWidget.verticalHeader().setCascadingSectionResizes(False)
        self.retakeWidget.verticalHeader().setDefaultSectionSize(30)

        self.horizontalLayout_3.addWidget(self.retakeWidget)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.line_2 = QFrame(self.widget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.imageBtn = QPushButton(self.widget)
        self.imageBtn.setObjectName(u"imageBtn")
        self.imageBtn.setFocusPolicy(Qt.NoFocus)

        self.horizontalLayout.addWidget(self.imageBtn)

        self.contactBtn = QPushButton(self.widget)
        self.contactBtn.setObjectName(u"contactBtn")
        self.contactBtn.setFocusPolicy(Qt.NoFocus)
        self.horizontalLayout.addWidget(self.contactBtn)

        self.linkBtn = QPushButton(self.widget)
        self.linkBtn.setObjectName(u"linkBtn")
        self.linkBtn.setFocusPolicy(Qt.NoFocus)
        self.horizontalLayout.addWidget(self.linkBtn)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.noteEdit = RVNoteWidget.NTextEdit(self.widget)
        self.noteEdit.setObjectName(u"noteEdit")

        self.horizontalLayout_2.addWidget(self.noteEdit)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.pushNoteBtn = QPushButton(self.widget)
        self.pushNoteBtn.setObjectName(u"pushNoteBtn")
        self.pushNoteBtn.setMinimumSize(QSize(0, 30))
        self.horizontalLayout_6.addWidget(self.pushNoteBtn)


        self.verticalLayout_3.addLayout(self.horizontalLayout_6)

        self.verticalLayout_3.setStretch(2, 1)
        self.verticalLayout_3.setStretch(5, 10)

        self.verticalLayout_4.addLayout(self.verticalLayout_3)


        self.verticalLayout.addWidget(self.widget)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", "项目:", None))
        self.noteProject.setText(QCoreApplication.translate("Dialog", u"TextLabel", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", "名称:", None))
        self.noteFileInfo.setText(QCoreApplication.translate("Dialog", "TextLabel", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", "制作人员:", None))
        self.noteCreaters.setText(QCoreApplication.translate("Dialog", "TextLabel", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", "任务状态:", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", "审核方式", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", "返修阶段", None))
        self.imageBtn.setText("")
        self.contactBtn.setText("")
        self.linkBtn.setText("")
        self.pushNoteBtn.setText(QCoreApplication.translate("Dialog", u"\u53d1\u5e03", None))
    # retranslateUi

