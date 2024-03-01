from PySide6 import QtWidgets, QtCore, QtGui
from rv_widgets import rv_box
from dataclasses import dataclass
from rvcore import event_manager, utl
import configparser



@dataclass
class ItemData:
    entity: str = ""
    db: str = ""


class RVTreeItem:
    def __init__(self, data_list, parent=None) -> None:
        self.child_item_list = []
        self.parent_item = parent
        self.item_data = data_list
        self.has_save = False
        self.is_render = False
    
    def update_save_state(self,):
        self.is_render = not self.is_render
    
    def get_save_state(self):
        return self.is_render
    
    def append_child(self, tree_item):
        self.child_item_list.append(tree_item)
    
    def append_children(self, tree_item_list):
        self.child_item_list.extend(tree_item_list)
    
    def child_count(self):
        return len(self.child_item_list)
    
    def data(self, column):
        return self.item_data[column].entity
    
    def parent(self):
        return self.parent_item
    
    def row(self):
        if self.parent_item:
            return self.parent_item.child_item_list.index(self)
        else:
            return 0
        
    def columnCount(self):
        return len(self.item_data)
    
    def child(self, row):
        return self.child_item_list[row]
    
    def get_child_list(self):
        return self.child_item_list
            

class RVProjectModel(QtCore.QAbstractItemModel):
    database_filename = QtCore.Property(str)
    def __init__(self):
        self.root_item = RVTreeItem([ItemData("", "")])
        self.column_value = ["项目"]
        super().__init__()
    
    def beginResetModel(self) -> None:
        self.root_item = RVTreeItem([ItemData("", "")])
        return super().beginResetModel()
    
    def data(self, index: QtCore.QModelIndex, role: int = ...):
        if not index.isValid():
            return None
        if role != QtCore.Qt.ItemDataRole.DisplayRole:
            return None

        item = index.internalPointer()
        return item.data(index.column())
    
    def rowCount(self, parent: QtCore.QModelIndex) -> int:
        parent_item = None
        if parent.column() > 0:
            return 0
        if not parent.isValid():
            parent_item = self.root_item
        else:
            parent_item = parent.internalPointer()
        return parent_item.child_count()
    
    def columnCount(self, parent: QtCore.QModelIndex) -> int:

        if parent.isValid():
            return parent.internalPointer().columnCount()
        return self.root_item.columnCount()
    
    def headerData(self, section: int, orientation, role: int = ...):
        if (orientation == QtCore.Qt.Orientation.Horizontal and role == QtCore.Qt.ItemDataRole.DisplayRole):
            return self.root_item.data(section)
        return None
    
    def index(self, row: int, column: int, parent: QtCore.QModelIndex=...) -> QtCore.QModelIndex:
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()
        parent_item = None
        if not parent.isValid():
            parent_item = self.root_item
        else:
            parent_item = parent.internalPointer()
        return self.createIndex(row, column, parent_item.child(row))
        

    def parent(self, index: QtCore.QModelIndex):
        if not index.isValid:
            return QtCore.QModelIndex()
        child_item = index.internalPointer()
        parent_item = child_item.parent()
        if parent_item == self.root_item:
            return QtCore.QModelIndex()
        
        return self.createIndex(parent_item.row(), 0, parent_item)

class RVProjectTreeModel(RVProjectModel):
    
    def __init__(self):
        super().__init__()
    
    def get_all_session_items(self, state):
        result = []
        for project_item in self.root_item.get_child_list():
            result.extend([i for i in project_item.get_child_list() if i.get_save_state() == state])
        return result
        
        
class RVProjectTreeDelegate(QtWidgets.QStyledItemDelegate):
    
    def __init__(self, parent: QtWidgets.QWidget = None, supprot_root=False):
        super().__init__(parent)
        self.__supprot_root = supprot_root
        self.__item_size = QtCore.QSize(0,25)
        image1 = QtGui.QImage(r":/resources/save_32.png")
        image2 = QtGui.QImage(r":/resources/unsave_32.png")
        self.save_pixmap = QtGui.QPixmap(image1.scaled(20,20, aspectMode=QtCore.Qt.AspectRatioMode.KeepAspectRatio, mode=QtCore.Qt.TransformationMode.SmoothTransformation))
        self.unsave_pixmap = QtGui.QPixmap(image2.scaled(20,20, aspectMode=QtCore.Qt.AspectRatioMode.KeepAspectRatio, mode=QtCore.Qt.TransformationMode.SmoothTransformation))
    
    def sizeHint(self, option, index):
        return self.__item_size
    
    def paint(self, painter: QtGui.QPainter, option: QtWidgets.QStyleOptionViewItem, index: QtCore.QModelIndex) -> None:
        if index.parent().column() >= 0 and index.parent().row() >= 0 or self.__supprot_root:
            if option.state & QtWidgets.QStyle.StateFlag.State_MouseOver:
                if index.internalPointer().get_save_state():
                    QtWidgets.QApplication.style().drawItemPixmap(painter, self.get_rect(option), QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter, self.save_pixmap)
                else:
                    QtWidgets.QApplication.style().drawItemPixmap(painter, self.get_rect(option), QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter, self.unsave_pixmap)
            else:
                if index.internalPointer().get_save_state():
                    QtWidgets.QApplication.style().drawItemPixmap(painter, self.get_rect(option), QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter, self.save_pixmap)
            option.widget.update(index)
        super().paint(painter, option, index)
    
    def get_rect(self, option):
        if isinstance(option, QtCore.QRect):
            rect = option
        else:
            rect = option.rect
        return QtCore.QRect(rect.left() + rect.width() - 30, rect.top(), rect.width(), rect.height())
    
    def editorEvent(self, event: QtGui.QMouseEvent, model, option, index) -> bool:
        # if index.parent().column() >= 0 and index.parent().row() >= 0:
        #     if event.type() == QtCore.QEvent.Type.MouseButtonRelease:
        #         mouse_pos = event.pos()
        #         rect = self.get_rect(option)
        #         if rect.contains(mouse_pos):
        #             index.internalPointer().update_save_state()
        return super().editorEvent(event, model, option, index)
    

class RVProjectView(QtWidgets.QTreeView):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setMouseTracking(True)
        self.pre_index = None
        self.setup()
        
    def setup(self):
        model = RVProjectTreeModel()
        delegate = RVProjectTreeDelegate(self)
        self.setModel(model)
        self.data_init()
        self.setItemDelegateForColumn(0, delegate)
        self.setMouseTracking(True)
        self.clicked.connect(self.on_item_clicked)
        event_manager.EventManager.get_instance().add_callback("SessionSaveStateChangeEvent", self.update_favorite_box)
        event_manager.EventManager.get_instance().add_callback("FavoriteClickedEvent", self.select_session)
        event_manager.EventManager.get_instance().add_callback("InitFinishedEvent", self.update_favorite_box)
    
    def data_init(self):
        self.model().beginResetModel()
        
        saved_sessions = utl.get_saved_sessions_from_init()
        interface = utl.TWLib()
        data = interface.get_all_session()
        for data_dict in data:
            for project_entity, session_info_list in data_dict.items():
                item_data = ItemData(project_entity)
                item = RVTreeItem([item_data], self.model().root_item)
                for child_info in session_info_list:
                    session = child_info.get("ani.entity_concat")
                    child_data = ItemData(child_info.get("ani.entity_concat"))
                    child = RVTreeItem([child_data], item)
                    if session in saved_sessions:
                        child.update_save_state()
                    item.append_child(child)
                self.model().root_item.append_child(item)
        self.model().endResetModel()

    def select_session(self, data_dict):
        current_index = self.currentIndex()
        session = data_dict.get("session")
        row_count = self.model().rowCount(QtCore.QModelIndex())
        for row in range(row_count):
            index = self.model().index(row, 0, QtCore.QModelIndex())
            for child_row in range(self.model().rowCount(index)):
                session_index = self.model().index(child_row, 0, index)
                if session == session_index.data():
                    self.setCurrentIndex(session_index)
                    self.on_item_clicked(session_index)
                    return
        
    def on_item_clicked(self, index: QtCore.QModelIndex):
        if index.parent().column() >= 0:
            event_manager.EventManager.get_instance()["AniChangeEvent"].emit({"ModelIndex": index})
    
    def update_favorite_box(self, *args):
        event_manager.EventManager.get_instance()["ProjectSaveStateChangeEvent"].emit({"child_item_list":self.model().get_all_session_items(True)})
        self.__save_ini()
        
    def mouseReleaseEvent(self, event) -> None:
        #self.itemDelegateForColumn(0).re
        index = self.indexAt(event.pos())
        if index.parent().column() >= 0 and index.parent().row() >= 0:
            if event.type() == QtCore.QEvent.Type.MouseButtonRelease:
                rect = self.visualRect(index)
                image_rect = self.itemDelegateForColumn(0).get_rect(rect)
                mouse_pos = event.pos()
                if image_rect.contains(mouse_pos):
                    index.internalPointer().update_save_state()
                    event_manager.EventManager.get_instance()["ProjectSaveStateChangeEvent"].emit({"child_item_list":self.model().get_all_session_items(True)})
                    self.__save_ini()
                else:
                    return super().mouseReleaseEvent(event)
        else:
            return super().mouseReleaseEvent(event)

    def __save_ini(self):
        config = configparser.ConfigParser()
        session = [i.data(0) for i in self.model().get_all_session_items(True)]
        
        config["Setting"] = {
        "Sessions": session if session else []
        }
        file_path = utl.PathData.get_ini_path()
        with open(file_path, "w", encoding="utf-8") as f:
            config.write(f)
    
    def update_widget(self):
        self.data_init()
        ...
        
def get_box():
    main_widget = RVProjectView()
    main_widget.updateGeometry()
    box = rv_box.RVSepBox(main_widget, None, "项目列表", update=True)
    return box