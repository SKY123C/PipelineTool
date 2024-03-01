
from PySide6 import QtCore


class RVThread(QtCore.QThread):
    def __init__(self, time_consuming_task, *args) -> None:
        super().__init__()
        self.__task = time_consuming_task
        self.task_args = args
        
        
    def run(self):
        self.__task(*self.task_args)