import sys
import os
import logging

"C:\CgTeamWork_v7\python\py3\DLLs"
os.environ['RV_SUPPORT_PATH'] = os.path.join(os.path.dirname(__file__), 'RVPlugin')
REQUIRE_PATH = [os.path.join(os.path.dirname(__file__), 'rvcore/network'), 
                os.path.dirname(__file__), 
                r'C:/CgTeamWork_v7/bin/base',
                os.path.join(os.path.dirname(__file__), 'Lib/site-packages')]
#os.chdir('C:/CgTeamWork_v7/bin/cgtw')
for i in REQUIRE_PATH:
    sys.path.insert(0, i)
sys.path.extend(REQUIRE_PATH)
def register_log():
    logger = logging.getLogger("RVPlayView")
    logger.setLevel(logging.DEBUG)
    log_path = os.path.dirname(__file__)
    log_name = os.path.join(log_path, 'rvlog.log')
    fh = logging.FileHandler(log_name, mode='a', encoding='utf-8')
    formatter = logging.Formatter('%(asctime)s-%(name)s-%(filename)s-[line:%(lineno)d]'
                                        '-%(levelname)s-[日志信息]: %(message)s',
                                        datefmt='%a, %d %b %Y %H:%M:%S')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    sys.excepthook = handle_exception
    logger.warning(str(sys.path))
    
def handle_exception(type, value, traceback):
    logger = logging.getLogger("RVPlayView")
    logger.error("程序BUG日志", exc_info=(type, value, traceback))
register_log()

import socket
import traceback
from PySide6 import QtWidgets
import qdarktheme
import cgtw2
from pathlib import Path
import argparse
import importlib
import rv_resources
import logging
from rv_ui import main_ui
from rvcore.base_classes import base_command
from rvcore import (utl, init_commands,)

app = QtWidgets.QApplication(sys.argv)
qdarktheme.setup_theme("light")


def checkTW():
    try:
        cgtw2.tw()
    except Exception as e:
        traceback.print_exc()
        QtWidgets.QMessageBox.about(None, "警告", "请登录CGTeamWork")
    else:
        return True

def checkSingleProcess():
    try:
        host ='127.0.0.1'
        port = utl.get_main_net_port()
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.settimeout(20)
        s.connect((host, port))
        s.close()
        QtWidgets.QMessageBox.about(None, "警告", "另外一个RVTool已经打开")
        return False
    except Exception as e:
        print("Connect Error")
        print(str(e))
        return True
    
def register_commandline():
    logger = logging.getLogger("RVPlayView")
    parser = argparse.ArgumentParser(description='Demo of argparse')
    win_command_path = Path(__file__).parent.joinpath("Plugins/CommandLine")
    if not win_command_path.exists():
        return
    for file in win_command_path.iterdir():
        if file.is_file() and str(file).endswith(".py"):
            importlib.import_module(f"Plugins.CommandLine.{file.stem}")
    parser.add_argument("--db")
    parser.add_argument("--module")
    parser.add_argument("--mt")
    parser.add_argument("--taskId")
    # 互斥
    group1 = parser.add_mutually_exclusive_group()
    for subclass in base_command.RVCommand.__subclasses__():
        group1.add_argument(f"-{subclass.shot_name}", f"--{subclass.long_name}", action='store_true')
    special_args = None
    if len(sys.argv) == 2 and "rvtool.azure://" in sys.argv[1]:
        special_args = sys.argv[1].rstrip("/").replace("rvtool.azure://", "").replace("%20", " ").split(" ")
    args = parser.parse_args(special_args)
    logger.warning(special_args)
    for subclass in base_command.RVCommand.__subclasses__():
        if hasattr(args, subclass.long_name) and getattr(args, subclass.long_name):
            subclass.run(args)

if __name__=='__main__':
    if len(sys.argv) > 1:
        register_commandline()
    else:
        init_commands.execute()
        if checkSingleProcess() and checkTW():
            QtWidgets.QApplication.setQuitOnLastWindowClosed(False)
            window = main_ui.RVMainWindow()
            window.show()
            sys.exit(app.exec())