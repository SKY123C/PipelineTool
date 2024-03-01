import rv
import rv.qtutils
from PySide2 import QtGui, QtCore, QtWidgets, QtUiTools
import os
from rv import commands as rvc
import sys
REQUIRE_PATH = [
    os.path.dirname(__file__),
    os.path.join(os.path.dirname(__file__), "CGTeamWork"),
    r'C:/CgTeamWork_v7/bin/base',
    r'C:/CgTeamWork_v7/bin/cgtw'
]
sys.path.extend(REQUIRE_PATH)
from CGTeamWork import noteDockWidget


class TWNote(rv.rvtypes.MinorMode):


    def __init__(self):
        rv.rvtypes.MinorMode.__init__(self)
        self.init("TWNote", None, None)
        self.note_widget = noteDockWidget.NoteDockWidget()
        self.note_widget.close_state.connect(self.set_toggle_state)
        rvSessionWindow = rv.qtutils.sessionWindow()
        rvSessionWindow.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.note_widget)

    def activate(self):
        rv.rvtypes.MinorMode.activate(self)
        self.note_widget.show()
    
    def deactivate(self):
        rv.rvtypes.MinorMode.deactivate(self)
        self.note_widget.hide()

    def set_toggle_state(self):
        self.toggle()
        
def createMode():
    "Required to initialize the module. RV will call this function to create your mode."
    return TWNote()