from PySide6 import QtCore, QtWidgets
from PySide6 import QtWidgets, QtGui
from rv_widgets import rv_box
from rvcore import utl
import enum

class FilterState(enum.Enum):
    ...

class FilterWidget(QtWidgets.QWidget):
    update_item_state = QtCore.Signal(dict)
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setup()
        self.__data = {}
    
    def setup(self):
        self.setContentsMargins(0,-1,0,0)
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(0,0,0,0)
        self.fileter_tree = QtWidgets.QTreeWidget(self)
        self.main_widget = rv_box.RVSepBox(self.fileter_tree, title="筛 选")
        self.main_widget.setContentsMargins(0,0,0,0)
        self.main_widget.set_checkable(False)
        self.main_widget.set_icon(QtGui.QIcon(r":/resources/filter_16.png"))
        self.main_layout.addWidget(self.main_widget)
        self.setMaximumWidth(0)
        self.fileter_tree.setColumnCount(1)
        #self.fileter_tree.setHeaderHidden(True)
        self.fileter_tree.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.ContiguousSelection)
    
    
    def init_tree(self, src_data_list):
        self.fileter_tree.clear()
        interface = utl.TWLib()
        self.__data = {}
        for sign in interface.get_sign_list():
            if not sign.get_display_state():
                continue
            label = sign.get_label()
            value = sign.get_sign().replace(".", "_")
            str_list = []
            self.__data[value] = {"label": label, "str_list": str_list}
            for item_list in src_data_list:
                for item in item_list:
                    item_data = item[0] if isinstance(item, list) else item
                    data_list = getattr(item_data, f"get_{value}")()
                    for data_str in data_list:
                        for data in data_str.split(","):
                            if data not in str_list:
                                str_list.append(data)
        status_color_dict = interface.get_status()
        for sign, value_dict in self.__data.items():
            value_list = value_dict.get("str_list")
            label = value_dict.get("label")
            root_node = QtWidgets.QTreeWidgetItem(self.fileter_tree)
            root_node.setData(0, QtCore.Qt.ItemDataRole.UserRole, sign)
            root_node.setCheckState(0, QtCore.Qt.CheckState.Checked)
            root_node.setFlags(QtCore.Qt.ItemFlag.ItemIsAutoTristate | QtCore.Qt.ItemFlag.ItemIsUserCheckable | QtCore.Qt.ItemFlag.ItemIsEnabled)
            root_node.setText(0, label)
            for value in value_list:
                node = QtWidgets.QTreeWidgetItem(root_node)
                node.setCheckState(0, QtCore.Qt.CheckState.Checked)
                if color := status_color_dict.get(value):
                    node.setForeground(0, QtGui.QColor(color))
                node.setToolTip(0, value)
                node.setText(0, value)
        self.fileter_tree.itemChanged.connect(lambda x:self.check_changed(x))
        
    def check_changed(self, item):
        current_data = self.get_current_tree_data()
        for sign, data_dict in current_data.items():
            dst_data_list = data_dict.get("str_list")
            if sign not in self.__data or len(self.__data.get(sign).get("str_list")) != len(dst_data_list):
                self.__data = current_data
                self.update_item_state.emit(self.__get_data_dict())
                break
            src_data_list = self.__data.get(sign).get("str_list")
            for value in dst_data_list:
                if value not in src_data_list:
                    self.__data = current_data
                    self.update_item_state.emit(self.__get_data_dict())
                    return
    
    def __get_data_dict(self):
        result = {}
        for sign, data_dict in self.__data.items():
            result[sign] = data_dict.get("str_list")
        return result
    
    def get_current_tree_data(self):
        result = {}
        for row in range(self.fileter_tree.topLevelItemCount()):
            root_node = self.fileter_tree.topLevelItem(row)
            sign = root_node.data(0, QtCore.Qt.ItemDataRole.UserRole)
            label = root_node.text(0)
            label_list = []
            result[sign] = {"label": label, "str_list": label_list}
            if root_node.checkState(0) == QtCore.Qt.CheckState.Unchecked:
                continue
            for child_row in range(root_node.childCount()):
                child_item = root_node.child(child_row)
                if child_item.checkState(0) == QtCore.Qt.CheckState.Checked:
                    label_list.append(child_item.text(0))
        return result
    
    def get_root_item_by_sign(self, sign):
        for row in range(self.fileter_tree.topLevelItemCount()):
            root_node = self.fileter_tree.topLevelItem(row)
            data = root_node.data(0, QtCore.Qt.ItemDataRole.UserRole)
            if data == sign:
                return root_node
    
    def set_status_check_state(self, dst_data_dict):
        for dst_sign, dst_value_list in dst_data_dict.items():
            root_node = self.get_root_item_by_sign(dst_sign)
            if not root_node:
                continue
            for child_row in range(root_node.childCount()):
                child_item = root_node.child(child_row)
                if child_item.checkState(0) == QtCore.Qt.CheckState.Unchecked and child_item.text(0) in dst_value_list :
                    child_item.setCheckState(0, QtCore.Qt.CheckState.Checked)
                    return
                elif child_item.checkState(0) == QtCore.Qt.CheckState.Checked and child_item.text(0) not in dst_value_list:
                    child_item.setCheckState(0, QtCore.Qt.CheckState.Unchecked)
                    return
    
    def __extend_tree(self):
        
        ...