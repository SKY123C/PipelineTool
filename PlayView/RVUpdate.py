import sys
import os
sys.path.extend([os.path.dirname(__file__)])
import logging
def init_log():
    logger = logging.getLogger()
    logger.setLevel(logging.WARNING)
    log_path = os.path.dirname(__file__)
    log_name = os.path.join(log_path, 'rvlog.log')
    fh = logging.FileHandler(log_name, mode='a', encoding='utf-8')
    formatter = logging.Formatter('%(asctime)s-%(name)s-%(filename)s-[line:%(lineno)d]'
                                        '-%(levelname)s-[日志信息]: %(message)s',
                                        datefmt='%a, %d %b %Y %H:%M:%S')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    logger.addHandler(stream_handler)
init_log()

def handle_exception(type, value, traceback):
    logger = logging.getLogger()
    logger.error("程序BUG日志", exc_info=(type, value, traceback))

sys.excepthook = handle_exception
import rv_resources
from rv_widgets.UI import ui_rv_update
from PySide6 import QtWidgets, QtCore, QtGui
from rv_widgets import rv_utl_widgets
import zipfile
import time
import socket
import json
import winreg
import requests


def start_rvtool():
    rvtool_path = os.path.dirname(__file__)
    QtCore.QProcess.startDetached(os.path.join(rvtool_path, "RVToolMain.exe"))
    sys.exit()


class UpdateThread(QtCore.QThread):

    process = QtCore.Signal(str)
    process_finished = QtCore.Signal(str)
    successed = QtCore.Signal()
    def __init__(self) -> None:
        super().__init__()

    def run(self) -> None:
        self.delete_instance()
        time.sleep(2)
        server_path = r"\\10.236.200.20\UE_Lib\tools\TA\RVTool"
        try:
            rvtool_path = os.path.dirname(__file__)
            if os.path.exists(server_path):
                time.sleep(2)
                zip_file_path = os.path.join(server_path, 'RVTool.zip')
                check = zipfile.is_zipfile(zip_file_path)
                if check:
                    zip_file = zipfile.ZipFile(zip_file_path)
                    all_file_list = zip_file.namelist()
                    for index, fname in enumerate(all_file_list):
                        zip_file.extract(fname, rvtool_path)
                        self.process.emit(str(round(index/len(all_file_list))*100) + "%")
            self.successed.emit()
        except Exception as e:
            log = logging.getLogger()
            log.error(f"更新日志:{str(e)}")
            self.process_finished.emit("更新失败，请查看日志获取更多信息")
            time.sleep(2)

    def delete_instance(self):
        while True:
            try:
                host ='127.0.0.1'
                port = 32145
                s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                s.settimeout(20)
                s.connect((host, port))
                s.send("Quit".encode('utf-8'))
            except Exception as e:
                break

class RVUpdateWidget(QtWidgets.QWidget, ui_rv_update.Ui_Form):
    
    update_success = QtCore.Signal()
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setObjectName("RVUpdate")
        self.setup()
        self.post_init()
        
    def post_init(self):
        self.update_thread = UpdateThread()
        self.update_thread.process.connect(lambda process:self.set_process_number(process))
        self.update_thread.process_finished.connect(lambda message:self.set_process_number(message))
        self.update_thread.successed.connect(lambda: self.update_success.emit())
        self.update_thread.finished.connect(start_rvtool)
    
    def setup(self):
        self.setWindowIcon(QtGui.QIcon(":/resources/icon.ico"))
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint|QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowTitle("更新")
        self.setStyleSheet("#main_frame.QFrame{border-image:url(:/resources/update_back.png);border:1px solid #161A1E;border-radius:5px;padding:5px 4px;}")
        #self.update_image.setScaledContents(False)
        self.update_image.setScaledContents(False)
        self.update_image.setFixedSize(QtCore.QSize(50,50))
        self.update_image.setStyleSheet("QLabel#update_image{border-image:url(:/resources/rocket.png)}")

        p = QtGui.QPalette()
        p.setColor(QtGui.QPalette.Base, QtGui.QColor(29, 41, 56, 180))
        self.textEdit.setPalette(p)
        p = QtGui.QPalette()
        p.setColor(QtGui.QPalette.ColorRole.WindowText, QtGui.QColor(255,255,255, 180))
        self.display_label.setPalette(p)
        p = QtGui.QPalette()
        p.setColor(QtGui.QPalette.ColorRole.WindowText, QtGui.QColor(255,255,255, 140))
        self.new_version_label.setPalette(p)
        self.cancel_updatebtn.setStyleSheet("QPushButton#cancel_updatebtn{background:rgba(55, 61, 65, 240);border-radius:5px;border:1px}\
                                            QPushButton#cancel_updatebtn:hover{border: 1px solid rgb(55, 30, 65);}")
        self.assign_update_btn.setStyleSheet("QPushButton#assign_update_btn{background:rgba(2, 191, 255, 200);border-radius:5px;border:1px}\
                                            QPushButton#assign_update_btn:hover{border: 1px solid rgb(2, 100, 255);}")
        self.textEdit.setFont(QtGui.QFont("open sans", 12, 2))
        self.process_frame = QtWidgets.QFrame()
        process_layout = QtWidgets.QVBoxLayout(self.process_frame)
        self.cancel_updatebtn.clicked.connect(self.start)
        self.assign_update_btn.clicked.connect(self.start_update)
        self.process = rv_utl_widgets.GifLabel(self)
        self.process_label = QtWidgets.QLabel()
        self.process_label.setPalette(p)
        process_layout.addWidget(self.process, 0, QtCore.Qt.AlignCenter)
        process_layout.addWidget(self.process_label, 0, QtCore.Qt.AlignCenter)
        self.verticalLayout_7.addWidget(self.process_frame, 0,QtCore.Qt.AlignCenter)
        self.process_frame.hide()
        self.textEdit.setReadOnly(True)
        
    def start(self):
        self.close()
        start_rvtool()
    
    def start_update(self):
        self.switch()
        self.update_thread.start()
    
    def switch(self):
        self.update_frame.hide()
        self.process_frame.show()
         
    def set_process_number(self, number):
        self.process_label.setText(number)

    def set_new_version_content(self, text):
        self.textEdit.setMarkdown(text)


class RVUpdate:
    
    def __init__(self):
        self.update_widget = RVUpdateWidget()
        self.current_version = None
        self.check()
        
    def check(self):
        content_path = r"\\10.236.200.20/UE_Lib/tools/TA/RVTool/RVToolContent.md"
        try:
            current_version_text = self.read_version()
            response = requests.request("get", "http://10.236.11.19:8023/RV")
            if response.status_code != 200:
                self.start_rvtool()
            else:
                source_version_text = str(json.loads(response.text).get("version", ""))
                self.update_widget.update_success.connect(self.set_version)
                if source_version_text and current_version_text != source_version_text:
                    print(source_version_text)
                    self.current_version = source_version_text
                    self.update_widget.new_version_label.setText("V" + source_version_text)
                    with open(content_path, "r", encoding="utf-8") as f3:
                        self.update_widget.set_new_version_content(f3.read())
                    self.update_widget.show()
                else:
                    #raise
                    self.start_rvtool()
        except Exception as e:
            logger = logging.getLogger()
            logger.error(str(e))
            self.start_rvtool()
    
    def start_rvtool(self):
        start_rvtool()
    
    def read_version(self):
        logger = logging.getLogger()
        command_key = self.get_winreg()
        result = "0"
        try:
            result = winreg.QueryValueEx(command_key, "version")
            result = result[0]
        except Exception as e:
            logger.warning(str(e))
        return result
    
    def get_winreg(self):
        return winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r"RVTool.Azure", 0, winreg.KEY_ALL_ACCESS)
    
    def set_version(self):
        if self.current_version:
            command_key = self.get_winreg()
            winreg.SetValueEx(command_key, "version", 0, winreg.REG_SZ, str(self.current_version))
    
        
app = QtWidgets.QApplication(sys.argv)

update = RVUpdate()

sys.exit(app.exec())