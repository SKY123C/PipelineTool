from typing import Optional
from PySide6 import QtCore, QtWidgets, QtGui
import PySide6.QtCore


class RVSepBox(QtWidgets.QWidget):
    hide_signal = QtCore.Signal(bool)
    def __init__(self, main_widget: QtWidgets.QWidget, parent: QtWidgets.QWidget=None, title="", toolbar=None, update=False) -> None:
        super().__init__(parent)
        self.__display_state = True
        self.update_widget = update
        self.main_widget = main_widget
        self.main_widget.setMinimumSize(QtCore.QSize(1,1))
        self.title = title
        self.__icon = {}
        self.__default_icon = {True: QtGui.QIcon(r":/resources/arrow_up.png"), False: QtGui.QIcon(r":/resources/arrow_down.png")}
        self.setup()
    
    def set_checkable(self, result):
        self.hide_button.setCheckable(result)
        #self.hide_button.setChecked(True)
    def set_icon(self,icon1, icon2=None):
        self.__icon[True] = icon1
        self.__icon[False] = icon2
        self.hide_button.setIcon(icon1)
        
    def get_display_state(self):
        return self.__display_state
    
    def setup(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(0,0,0,0)
        tool_bar = self.create_default_toolbar()
        
        self.main_layout.addWidget(tool_bar, 0, QtCore.Qt.AlignmentFlag.AlignTop)
        self.main_layout.addWidget(self.main_widget, 1)
    
    def sizeHint(self) :
        return QtCore.QSize(0, 0)
    
    def create_default_toolbar(self):
        tool_bar = QtWidgets.QWidget(self)
        tool_bar.setObjectName("rv_box_tool_bar")
        tool_bar.setStyleSheet("#rv_box_tool_bar{background-color:rgb(238, 238, 238)}")
        layout = QtWidgets.QHBoxLayout(tool_bar)
        label = QtWidgets.QLabel()
        label.setText(self.title)
        self.hide_button = QtWidgets.QPushButton()
        self.hide_button.setCheckable(True)
        self.hide_button.setChecked(True)
        self.hide_button.setIcon(QtGui.QIcon(r":/resources/arrow_up.png"))
        self.hide_button.clicked.connect(self.__hide_widget)
        layout.addWidget(label)
        if self.update_widget:
            self.update_btn = QtWidgets.QPushButton()
            self.update_btn.setObjectName("update_btn")
            #self.update_btn.setStyleSheet("#update_btn{border-width:0px;}")
            self.update_btn.setIcon(QtGui.QIcon(r":/resources/refresh_no_16.png"))
            if hasattr(self.main_widget, "update_widget"):
                self.update_btn.clicked.connect(self.main_widget.update_widget)
            layout.addWidget(self.update_btn, 1, QtCore.Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.hide_button, 0, QtCore.Qt.AlignmentFlag.AlignRight)
        return tool_bar
        
    def __hide_widget(self, hide_state):
        self.__display_state = hide_state
        icon = None
        if self.__icon:
            if self.hide_button.isCheckable():
                icon = self.__icon[hide_state]
            else:
                icon = self.__icon[True]
            ...
        else:
            icon = self.__default_icon[hide_state]
        self.hide_button.setIcon(icon)
        self.hide_signal.emit(hide_state)
    
    @property
    def widget(self):
        return self.main_widget