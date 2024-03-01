from Widgets import RVNoteWidget
from RVControllers import RVnoteControll
from PySide2 import QtWidgets, QtCore


class NoteDockWidget(QtWidgets.QDockWidget):
    close_state = QtCore.Signal()
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Push Note")
        self.setWindowFlags(QtCore.Qt.Tool)
        self.note_widget = RVNoteWidget.ENoteDialog(self)
        self.note_controll = RVnoteControll.NoteControll(self.note_widget)
        self.setWidget(self.note_widget)
        self.setFloating(True)
        self.topLevelChanged.connect(self.refresh)
    
    def refresh(self, is_change):
        self.resize(self.width()+1, self.height())

    def show(self, **args):
        self.note_controll.init()
        super().show(**args)
        self.resize(self.width()+1, self.height())
    
    def closeEvent(self, event):
        self.close_state.emit()