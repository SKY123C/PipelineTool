# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'rv_updateEPpyCP.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication,QMetaObject, QSize)
from PySide6.QtGui import (QFont)
from PySide6.QtWidgets import (QFrame, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QTextEdit, QVBoxLayout)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(529, 448)
        self.verticalLayout_2 = QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.main_frame = QFrame(Form)
        self.main_frame.setObjectName(u"main_frame")
        self.main_frame.setMinimumSize(QSize(0, 30))
        self.main_frame.setFrameShape(QFrame.StyledPanel)
        self.main_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.main_frame)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 10, 0, 0)
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(10, -1, 10, -1)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(15, 20, -1, 20)
        self.update_image = QLabel(self.main_frame)
        self.update_image.setObjectName(u"update_image")
        self.update_image.setScaledContents(False)

        self.horizontalLayout_3.addWidget(self.update_image)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.display_label = QLabel(self.main_frame)
        self.display_label.setObjectName(u"display_label")
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setStyleStrategy(QFont.PreferDefault)
        self.display_label.setFont(font)

        self.verticalLayout_5.addWidget(self.display_label)

        self.new_version_label = QLabel(self.main_frame)
        self.new_version_label.setObjectName(u"new_version_label")
        font1 = QFont()
        font1.setPointSize(10)
        self.new_version_label.setFont(font1)

        self.verticalLayout_5.addWidget(self.new_version_label)


        self.horizontalLayout_3.addLayout(self.verticalLayout_5)

        self.horizontalLayout_3.setStretch(0, 2)
        self.horizontalLayout_3.setStretch(1, 8)

        self.verticalLayout_7.addLayout(self.horizontalLayout_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(8, 10, 8, -1)
        self.textEdit = QTextEdit(self.main_frame)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setFrameShape(QFrame.NoFrame)

        self.horizontalLayout.addWidget(self.textEdit)


        self.verticalLayout_7.addLayout(self.horizontalLayout)

        self.update_frame = QFrame(self.main_frame)
        self.update_frame.setObjectName(u"update_frame")
        self.update_frame.setFrameShape(QFrame.StyledPanel)
        self.update_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.update_frame)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 10, 0, 10)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(5, 0, 5, 0)
        self.cancel_updatebtn = QPushButton(self.update_frame)
        self.cancel_updatebtn.setObjectName(u"cancel_updatebtn")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cancel_updatebtn.sizePolicy().hasHeightForWidth())
        self.cancel_updatebtn.setSizePolicy(sizePolicy)
        self.cancel_updatebtn.setMinimumSize(QSize(130, 40))

        self.horizontalLayout_2.addWidget(self.cancel_updatebtn)

        self.assign_update_btn = QPushButton(self.update_frame)
        self.assign_update_btn.setObjectName(u"assign_update_btn")
        sizePolicy.setHeightForWidth(self.assign_update_btn.sizePolicy().hasHeightForWidth())
        self.assign_update_btn.setSizePolicy(sizePolicy)
        self.assign_update_btn.setMinimumSize(QSize(130, 40))

        self.horizontalLayout_2.addWidget(self.assign_update_btn)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)


        self.verticalLayout_7.addWidget(self.update_frame)


        self.verticalLayout_8.addLayout(self.verticalLayout_7)


        self.verticalLayout.addWidget(self.main_frame)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.update_image.setText("")
        self.display_label.setText(QCoreApplication.translate("Form", u"\u53d1\u73b0\u65b0\u7248\u672c", None))
        self.new_version_label.setText(QCoreApplication.translate("Form", u"V1.4.0", None))
        self.cancel_updatebtn.setText(QCoreApplication.translate("Form", u"\u6682\u4e0d\u66f4\u65b0", None))
        self.assign_update_btn.setText(QCoreApplication.translate("Form", u"\u7acb\u5373\u66f4\u65b0", None))
    # retranslateUi

