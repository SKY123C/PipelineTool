
from rvcore.base_classes import base_action
from rvcore import utl
from PySide6 import QtCore, QtWidgets
import os
import pathlib


class OpenDirAction(base_action.TableAction):
    active = True
    def __init__(self, index_list: list[QtCore.QModelIndex], table: QtWidgets.QTableView) -> None:
        super().__init__("打开文件夹", index_list=index_list, table=table)
        data = index_list[0].data(QtCore.Qt.ItemDataRole.UserRole)
        self.shot_entity = data.get_shot_entity(is_package=True, repeat=True)
        self.task_entity = data.get_task_entity(is_package=True)
        self.db_entity = data.get_db_entity(is_package=True, repeat=True)
    
    def action_callback(self, *args):

        self.openDirectory()
    
    def openDirectory(self):
        for index in self.get_model_index_List():
            item_data = index.data(QtCore.Qt.ItemDataRole.UserRole)
            for item in item_data.get_all_tw_data():
                print(item.file)
                path = os.path.normpath(item.file)
                # path = path.replace(r'\\', '\\')
                # path = r"\\" + path.strip("\\")
                print(path)
                if os.path.exists(path):
                    if os.path.isfile(path):
                        os.startfile(os.path.dirname(path))
                    else:
                        os.startfile(path)
                else:
                    if item.get_cloud_state():
                        path = self.checkFileExits(path)
                        os.startfile(path)
                    else:
                        path = self.checkFileExits(path)
                        if path:
                            os.startfile(path)
    
    def checkFileExits(self, path):
        if not path:
            return ""
        elif os.path.exists(path):
            return path
        else:
            return self.checkFileExits(os.path.dirname(path))