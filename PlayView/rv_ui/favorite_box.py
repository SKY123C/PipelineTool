from PySide6 import QtCore, QtWidgets, QtGui
from rv_ui import project_box
from rv_widgets import rv_box
from rvcore import event_manager


class RVFavoriteBoxModel(project_box.RVProjectModel):
    
    def __init__(self):
        super().__init__()
    
    def data_init(self, item_list):
        self.root_item.get_child_list().clear()
        self.root_item.append_children(item_list)
    
    def rowCount(self, parent: QtCore.QModelIndex) -> int:
        if (parent.row() == -1):
            return len([i for i in self.root_item.get_child_list() if i.get_save_state()])
        return 0

    def data(self, index: QtCore.QModelIndex, role: int = ...):
        if not index.isValid():
            return None
        if role != QtCore.Qt.ItemDataRole.DisplayRole:
            return None
        item = index.internalPointer()
        return item.data(index.column())

    def index(self, row: int, column: int, parent: QtCore.QModelIndex=...) -> QtCore.QModelIndex:
        item_list = [i for i in self.root_item.get_child_list() if i.get_save_state()]
        if not parent.isValid():
            return self.createIndex(row, column, item_list[row])
            
    def parent(self, index: QtCore.QModelIndex):
        if index.isValid():
            return QtCore.QModelIndex()


class RVFavoriteBoxDelegate(project_box.RVProjectTreeDelegate):
    
    def __init__(self, parent: QtWidgets.QWidget = None, supprot_root=False):
        super().__init__(parent, supprot_root)
    
    def paint(self, painter: QtGui.QPainter, option: QtWidgets.QStyleOptionViewItem, index: QtCore.QModelIndex) -> None:
        ...
        
        #if index.internalPointer().get_save_state():
        super().paint(painter, option, index)
    

class RVFavoriteBox(QtWidgets.QTreeView):
    
    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        self.setup()
    
    def setup(self):
        model = RVFavoriteBoxModel()
        self.setModel(model)
        delegate = RVFavoriteBoxDelegate(self, supprot_root=True)
        self.setItemDelegateForColumn(0, delegate)
        self.setMouseTracking(True)
        event_manager.EventManager.get_instance().add_callback("ProjectSaveStateChangeEvent", self.refresh)
        self.clicked.connect(self.select_session)
    
    def select_session(self):
        index_list = self.selectionModel().selectedIndexes()
        event_manager.EventManager.get_instance()["FavoriteClickedEvent"].emit({"session": index_list[0].data()})
    
    def refresh(self, data_dict):
        data = data_dict.get("child_item_list")
        self.model().beginResetModel()
        self.model().data_init(data)
        self.model().endResetModel()

    def mouseReleaseEvent(self, event) -> None:
        #self.itemDelegateForColumn(0).re
        index = self.indexAt(event.pos())
        if index.column() >= 0 and index.row() >= 0:
            if event.type() == QtCore.QEvent.Type.MouseButtonRelease:
                rect = self.visualRect(index)
                image_rect = self.itemDelegateForColumn(0).get_rect(rect)
                mouse_pos = event.pos()
                if image_rect.contains(mouse_pos):
                    index.internalPointer().update_save_state()
                    event_manager.EventManager.get_instance()["SessionSaveStateChangeEvent"].emit({})
                else:
                    return super().mouseReleaseEvent(event)
        else:
            return super().mouseReleaseEvent(event)

    def focusOutEvent(self, event: QtGui.QFocusEvent) -> None:
        self.selectionModel().clearSelection()
        return super().focusOutEvent(event)


def get_box(a):
    main_widget = RVFavoriteBox()
    box = rv_box.RVSepBox(main_widget, None, "快速访问")
    return box