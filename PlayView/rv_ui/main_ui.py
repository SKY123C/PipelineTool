from typing import Optional
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import QObject
from rv_widgets import (rv_tabbar, rv_table)
from rv_ui import (project_box,
                   favorite_box,
                   )
from rvcore import event_manager, menu_manager, utl
import socket
event_manager.EventManager()
menu_manager.MenuManager()


class RVNetWork(QtCore.QThread):
    command = QtCore.Signal(str)
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.setObjectName("NetWork")
    
    def run(self):                    
        host = '127.0.0.1'
        port = utl.get_main_net_port()              
        self.s.bind((host, port))   
        self.s.listen(2)                
        while True:
            content, addr = self.s.accept()
            while True:
                try:
                    text = content.recv(1024)
                    if len(text):
                        self.command.emit(text.decode())
                    else:
                        content.close()
                except Exception as e:
                    print(str(e))
                    break    
    
    
class SystemTray(QtWidgets.QSystemTrayIcon):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.callback()
        self.setToolTip("RV关东煮")
        #self.setIcon(QtGui.QIcon(":/Resources/icons/icon.ico"))
        self.setIcon(QtGui.QIcon(":/resources/video_16.png"))
        self.setMenu()
        self.activated.connect(self.mouseClick)

    def callback(self):
        ...

    def mouseClick(self, reason):
        print(reason)
        if reason == QtWidgets.QSystemTrayIcon.ActivationReason.DoubleClick:
            self.parent().show()

    def setMenu(self):
        menu = QtWidgets.QMenu()
        self.a2 = QtGui.QAction('&退出(Exit)',triggered = self.quitApp)
        menu.addAction(self.a2)
        self.setContextMenu(menu)

    def quitApp(self):
        QtCore.QCoreApplication.instance().quit()
        
        
class RVMainWindow(QtWidgets.QMainWindow):
    
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.resize(1400,624)
        #self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowTitle("RV关东煮")
        self.setWindowIcon(QtGui.QIcon(":/resources/video_16.png"))
        #self.setWindowIcon(QtGui.QIcon(":/resources/update_back.png"))
        self.net_thread = RVNetWork()
        self.setup()

    def exec_command(self, content):
        if content == "Quit":
            self.close()
            self.system_tray.quitApp()
        ...
        
    def menu_init(self):
        menu_bar = self.menuBar()
        tooll_menu = menu_bar.addMenu("工具")
        action = tooll_menu.addAction("全 局 搜 索")
        help_menu = menu_bar.addMenu("帮助")
        action.triggered.connect(self.__open_global_search_window)
    
    def __open_global_search_window(self):
        
        ...
        
    def tray_init(self):
        self.system_tray = SystemTray(self)
    
    def show(self):
        super().show()
        self.system_tray.show()
        
    def setup(self):
        self.net_thread.start()
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)
        self.main_layout = QtWidgets.QSplitter(widget)
        self.main_layout.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.tool_layout = QtWidgets.QSplitter(self.main_layout)
        self.tool_layout.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.main_layout.addWidget(self.tool_layout)
        self.add_tab()
        self.add_tool_box()
        self.tool_layout.setCollapsible(0, False)
        layout.addWidget(self.main_layout)
        self.setCentralWidget(widget)
        self.statusbar_setup()
        self.main_layout.setSizes([100,500])
        event_manager.EventManager.get_instance()["InitFinishedEvent"].emit({})
        self.tray_init()
        self.menu_init()
        self.net_thread.command.connect(self.exec_command)
        
    def add_tool_box(self):
        project = project_box.get_box()
        favorite = favorite_box.get_box(self.tool_layout)
        project.hide_signal.connect(self.reset_tool_splitter)
        favorite.hide_signal.connect(self.reset_tool_splitter)
        self.tool_layout.addWidget(project)
        self.tool_layout.addWidget(favorite)
    
    def add_tab(self):
        widget = QtWidgets.QWidget()
        v_layout = QtWidgets.QVBoxLayout(widget)
        v_layout.setContentsMargins(5,0,0,0)
        tab = rv_tabbar.RVTabBar()
        v_layout.addWidget(tab, 0, QtCore.Qt.AlignmentFlag.AlignTop)
        table_container = rv_table.RVTableContainer()
        tab.deleted.connect(table_container.close_table)
        tab.created.connect(table_container.create_table)
        tab.currentChanged.connect(table_container.switch_table)
        v_layout.addWidget(table_container, 3)
        #v_layout.addStretch(0)
        self.main_layout.addWidget(widget)
        
    def reset_tool_splitter(self, is_hide):
        sender = self.sender()
        sizes = self.tool_layout.sizes()
        result = []
        for index in range(0, self.tool_layout.count()):
            widget = self.tool_layout.widget(index)
            result.append(widget.get_display_state())
        result = [True, True] if not any(result) else result
        self.tool_layout.setSizes(list(map(lambda x: 1000*x, result)))
    
    
    def statusbar_setup(self):
        ...
        self.statusBar()
        
    def closeEvent(self, event) -> None:
        self.system_tray.showMessage('RV关东煮','Hide Here', QtWidgets.QSystemTrayIcon.MessageIcon.Information, 10)