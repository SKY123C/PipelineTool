from rvcore.base_classes import base_manager, base_action
from rvcore.rv_system import base_event
from rvcore import utl
from PySide6 import QtGui, QtWidgets
import importlib
import pathlib
from rv_widgets.rv_actions import (
    open_dir, open_tw, play_action, switch
)




class MenuManager(base_manager.Manager):
    
    def __init__(self) -> None:
        super().__init__()
        self.__menu_map = {}
        self.load_all_actions()
    
    def register_menu(self, menu_name, menu: QtWidgets.QMenu):
        self.__menu_map[menu_name] = menu
    
    def show_menu(self, menu_name, menu_type, pos, **kwargs):
        menu: QtWidgets.QMenu = self.__menu_map.get(menu_name)
        menu.clear()
        action_list = self.get_all_action()
        actions = []
        for action_class in action_list:
            if menu_type in action_class.menu_type and action_class.active:
                action = action_class(**kwargs)
                if action.rule():
                    actions.append(action)
                
        if actions:
            menu.addActions(actions)
            menu.exec_(pos)

    
    def load_all_actions(self):
        ...
    
    def get_all_action(self, base_class=base_action.RVAction):
        subclasses = []
        for subclass in base_class.__subclasses__():
            subclasses.append(subclass)
            subclasses.extend(self.get_all_action(subclass))
        return subclasses