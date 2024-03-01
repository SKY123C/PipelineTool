
from rvcore.base_classes import base_action
from rvcore import utl
from PySide6 import QtCore


class OpenTWAction(base_action.TableAction):
    active = True
    def __init__(self, index_list: list[QtCore.QModelIndex], table) -> None:
        super().__init__("跳转TeamWork", index_list=index_list, table=table)
        data = index_list[0].data(QtCore.Qt.ItemDataRole.UserRole)
        self.shot_entity = data.get_shot_entity(is_package=True, repeat=True)
        self.task_entity = data.get_task_entity(is_package=True)
        self.db_entity = data.get_db_entity(is_package=True, repeat=True)
    
    def action_callback(self, *args):
        interface = utl.TWLib()
        result = interface.get_info(self.db_entity, "shot", utl.TWLib.ModuleType.TASK, [
            ["shot.entity", "=", self.shot_entity], "and",
            ["task.entity", "=", self.task_entity]
        ], ["task.id"], [])
        if result:
            interface.jump_teamwork(self.db_entity, result[0].get("task.id"), "shot", "task")
        
        return super().action_callback(*args)