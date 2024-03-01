from PySide6 import QtWidgets, QtCore
from rvcore import event_manager


class RVTabBar(QtWidgets.QTabBar):
    created = QtCore.Signal(dict)
    deleted = QtCore.Signal(int)
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setup()
        self.event_init()

    def event_init(self):
        event_manager.EventManager.get_instance().add_callback("AniChangeEvent", self.create_tab)

    def create_tab(self, info):
        tab_count = self.count()
        session = info.get("ModelIndex").data()
        db_entity = info.get("ModelIndex").parent().data()
        for index in range(tab_count):
            if self.tabText(index) == session:
                self.setCurrentIndex(index)
                break
        else:
            tab_index = self.addTab(session)
            self.created.emit({"session": session, "index": tab_index, "db_entity": db_entity})
            self.setCurrentIndex(tab_index)
            ...
            
    def setup(self):
        self.setExpanding(False)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.remove_tab_impl)
        #self.currentChanged.connect(lambda index: event_manager.EventManager.get_instance()["TabIndexChangeEvent"].emit({"session": self.tabText(index), "index": index, "db_entity": self.__tempdb_entity}))
    
    def remove_tab_impl(self, index):
        if self.count() > 1:
            self.removeTab(index)
            self.deleted.emit(index)
            self.setCurrentIndex(self.count() - 1)