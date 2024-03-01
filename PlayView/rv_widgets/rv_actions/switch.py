
from rvcore.base_classes import base_action
from rvcore import utl
from PySide6 import QtCore, QtWidgets


class SwitchAction(base_action.TableAction):
    active = True
    def __init__(self, index_list: list[QtCore.QModelIndex], table: QtWidgets.QTableView) -> None:
        super().__init__("切换路径", index_list=index_list, table=table)
        data = index_list[0].data(QtCore.Qt.ItemDataRole.UserRole)
        self.shot_entity = data.get_shot_entity(is_package=True, repeat=True)
        self.task_entity = data.get_task_entity(is_package=True)
        self.db_entity = data.get_db_entity(is_package=True, repeat=True)
    
    def action_callback(self, *args):

        self.table.switch_path(self.get_model_index_List())

    def rule(self):
        result = []
        for index in self.get_model_index_List():
            stage = self.table.model().headerData(index.column(), QtCore.Qt.Orientation.Horizontal, QtCore.Qt.ItemDataRole.DisplayRole)
            result.append(stage in utl.get_cloud_stage())
        return all(result)