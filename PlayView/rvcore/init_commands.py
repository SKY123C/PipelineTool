
import os
import time
import traceback
import logging

# 该部分代码需要更改
class Cmd(object):

    @staticmethod
    def deleteRVTool():
        while True:
            rv_tool_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "RVTool.exe")
            if os.path.exists(rv_tool_path):
                try:
                    os.remove(rv_tool_path)
                    break
                except Exception as e:
                    print(str(e))
            else:
                break
    
    @staticmethod
    def update():
        time.sleep(1)
        root_path = os.path.dirname(os.path.dirname(__file__))
        update_path = os.path.join(root_path, 'update.exe')
        if os.path.exists(update_path):
            update_new_path = os.path.join(root_path, 'RV关东煮.exe')
            try:
                update_old_path = os.path.join(os.path.join(root_path, 'update_old.exe'))
                if os.path.exists(update_new_path):
                    os.rename(update_new_path, update_old_path)
                os.rename(update_path, update_new_path)
                if os.path.exists(update_old_path):
                    os.remove(update_old_path)
            except:
                log = logging.getLogger("RVPlayView")
                log.warning(traceback.format_exc())
        
def execute():
    for callback in set(dir(Cmd))-set(dir(object)):
        callback_object = getattr(Cmd, callback)
        if callback not in ['__dict__', '__module__', '__weakref__'] and hasattr(callback_object, "__call__"):
            callback_object()