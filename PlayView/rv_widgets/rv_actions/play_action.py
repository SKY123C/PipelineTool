
from rvcore.base_classes import base_action
from rvcore import utl
import os
from PySide6 import QtCore
import json
from PySide6 import QtWidgets
import threading
import enum

class PlayMode(enum.Enum):
    DEFAULTLAYOUT = "defaultLayout"
    DEFAULTSEQUENCE = "defaultSequence"
    

class PlayAction(base_action.TableAction):
    port = 25124
    active = True
    def __init__(self, index_list: list[QtCore.QModelIndex], table) -> None:
        super().__init__("播放", index_list=index_list, table=table)
    
    def action_callback(self, *args):
        mode = self.get_play_mode(self.get_model_index_List())
        key_value = ["task_id", "task_task_leader_status", "shot_entity", "task_entity", 'task_last_submit_time', 'task_account']
        items_list = self.split_column(self.get_model_index_List(), key_value)
        files = [file_list for file_list in items_list.get("paths") if file_list]
        values = [file_list for file_list in items_list.get("values") if file_list]
        self.set_OsVarent(key_value)
        if not files:
            return
        self.checkRVPath(mode, files, values)
        
    def set_OsVarent(self, value_list):
        value_dict = dict.fromkeys(value_list, '')
        os.environ["TEAMWORKINFO"] = json.dumps(value_dict)
        
    def get_play_mode(self, index_List: list[QtCore.QModelIndex]):
        result = None
        if not index_List or len(index_List) < 2:
            result = PlayMode.DEFAULTSEQUENCE
        else:
            row_list = [i.row() for i in index_List]
            if len(row_list) == set(row_list):
                result = PlayMode.DEFAULTLAYOUT
            else:
                result = PlayMode.DEFAULTSEQUENCE
        return result.value

    def split_column(self, index_list: list[QtCore.QModelIndex], key_value):
        row_dict = {}
        # 收集每列的数据
        for index in index_list:
            column = index.column()
            row = index.row()

            if row in row_dict:
                info_dict = row_dict.get(row)
                info_dict["info_list"].append(index)
            else:
                row_dict[row] = {"info_list": [index]}
        
        new_row_dict = dict(sorted(row_dict.items()))
        result_path_list = []
        result_info_list = []
        count_list = [len(temp_info_dict.get("info_list")) for temp_info_dict in new_row_dict.values()]
        is_supplement = [count_list[i]==count_list[i+1] for i in range(0, len(count_list) - 1)]
        if all(is_supplement):
            for column_playlist in zip(*[i.get("info_list") for i in new_row_dict.values()]):
                temp_p_path, temp_p_info = self.get_package_path_info(column_playlist, key_value)
                result_path_list.append(temp_p_path)
                result_info_list.append(temp_p_info)
            
        else:
            tmp_list = [j for i in new_row_dict.values() for j in i.get("info_list")]
            temp_p_path, temp_p_info = self.get_package_path_info(tmp_list, key_value)
            result_path_list.append(temp_p_path)
            result_info_list.append(temp_p_info)
        return {'paths': result_path_list, 'values': result_info_list}
    

    def get_package_path_info(self, data_list, key_value):
        temp_p_path = []
        temp_p_info = []
        for index in data_list:
            data = index.data(QtCore.Qt.ItemDataRole.UserRole)
            path_list = data.get_file()
            value_list = self.get_value_list(index, key_value)
            path_list_dict = self.getRVRuleFiles(path_list, value_list)
            temp_p_path.extend([[i] for i in path_list_dict.get("paths")])
            temp_p_info.extend([list(i.items()) for i in path_list_dict.get("values")])
        return temp_p_path, temp_p_info
    
    def get_value_list(self, index: QtCore.QModelIndex, key_value):
        data = index.data(QtCore.Qt.ItemDataRole.UserRole)
        result = []
        for i in data.get_all_tw_data():
            value_dict = {}
            for value in key_value:
                value_dict[value] = getattr(i, value)
            value_dict["db_entity"] = data.get_db_entity(is_package=True, repeat=True)
            result.append(value_dict)
        return result
                
            
    def getRVRuleFiles(self, file_list, value_list):
        values = []
        paths = []
        for index, path in enumerate(file_list):
            #if os.path.exists(path) and path.replace('/', ''):
            value_dict = value_list[index]
            # if os.path.isdir(path):
            #     path = os.path.join(path, utl.get_sequence_string(path))
            paths.append(path)
            values.append(value_dict)
        return {"paths": paths,"values": values}
    
    def checkRVPath(self, mode, files, values):
        db_entity = self.get_model_index_List()[0].data(QtCore.Qt.ItemDataRole.UserRole).get_db_entity(is_package=True, repeat=True)
        rvPath = self.interface.get_software_path(db_entity, "RV")
        messageBox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, "警告", "请在TeamWork工具中设置正确的RV路径")
        if not rvPath and not os.path.exists(rvPath):
            messageBox.addButton(self.tr("    OK     "),QtWidgets.QMessageBox.YesRole)
            messageBox.exec_()
            return
        try:
            thread = threading.Thread(target=utl.rvCmd, args=(mode, files, values, rvPath, type(self).port,))
            thread.start()
            type(self).port += 1
        except Exception as e:
            print(str(e))
            messageBox.setText("连接RV失败")
            messageBox.exec_()