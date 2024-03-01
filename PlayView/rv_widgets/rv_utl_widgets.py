from PySide6 import QtWidgets, QtGui, QtCore
import functools



class RVSearch(QtWidgets.QLineEdit):

    def __init__(self, parent=None, **kwds) -> None:
        super().__init__(parent=parent)
        self.line_tool_action = QtGui.QAction()
        self.addAction(self.line_tool_action,QtWidgets.QLineEdit.ActionPosition.LeadingPosition)
        self.init(**kwds)
    
    def init(self, **kwds):
        icon_path = kwds.get("icon_path")
        self.setPlaceholderText(kwds.get("placeholder"))
        btn_fun = kwds.get("btn_fun")
        if icon_path:
            self.line_tool_action.setIcon(QtGui.QIcon(icon_path))
        
        if btn_fun:
            btn_fun = functools.partial(btn_fun, line=self)
            self.line_tool_action.triggered.connect(btn_fun)
            
        self.setClearButtonEnabled(True)


class GifLabel(QtWidgets.QLabel):

    def __init__(self, parent):
        self.gif_path = ":/resources/wait.gif"
        self.finished_icon_path = ":/resources/success.png"
        self.error_icon_path = ":/resources/error.png"
        super().__init__(parent=parent)
        self.setObjectName('imageplayer')
        self.mymovie = QtGui.QMovie(":/resources/wait.gif", QtCore.QByteArray(), self)
        self.setMovie(self.mymovie)
        #self.mymovie.setFileName(":/resources/loading_ad.gif")
        self.mymovie.setScaledSize(QtCore.QSize(50,50))
        self.mymovie.setCacheMode(QtGui.QMovie.CacheAll)
        self.mymovie.start()
 

    def switch(self, error=False):
        self.mymovie.stop()
        if error:
            self.mymovie.setFileName(self.error_icon_path)
        else:
            self.mymovie.setFileName(self.finished_icon_path)
        self.mymovie.start()