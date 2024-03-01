import sys
from typing import Optional
from PySide6 import QtWidgets, QtGui, QtCore
import mmap
import numpy as np



# 创建应用程序
app = QtWidgets.QApplication(sys.argv)    # sys.argv显示当前文件的目录位置以及其它参数的列表,将文件路径传递给对象用于构建应用程序
                                # sys.argv用于接收命令行参数    使用时argy[索引]
# 创建窗口
h = 240
w = int(240*1.7)
class Thread(QtCore.QThread):
    image_signal = QtCore.Signal(np.ndarray)
    def __init__(self) -> None:
        super().__init__()
    def run(self):
        
        while True:

            mmap_file1  = mmap.mmap(-1, int(h*w*4), tagname="Global\ForeSharedMemory", access=mmap.ACCESS_READ)
            mmap_file1.seek(0)
            uint8_data = np.frombuffer(mmap_file1.read(), dtype=np.uint8).reshape(h, w, 4)
            
            mmap_file2  = mmap.mmap(-1, int(h*w*4), tagname="Global\BackSharedMemory", access=mmap.ACCESS_READ)
            mmap_file2.seek(0)
            uint8_data2 = np.frombuffer(mmap_file2.read(), dtype=np.uint8).reshape(h, w, 4)
            uint8_data3 = uint8_data2.copy()
            mask = uint8_data[...,-1] <= 0
            uint8_data3[mask] = uint8_data[mask]
            #print(uint8_data2.shape)
            #np.where(uint8_data3 == 0, 255, uint8_data3)
            #print(result)
            self.image_signal.emit(np.where(uint8_data3 == 0, 255, uint8_data3))

class Widget(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        
        layout = QtWidgets.QVBoxLayout(self)
        self.label = QtWidgets.QLabel()
        layout.addWidget(self.label)
        self.thread = Thread()
        self.thread.image_signal.connect(self.set_pixmap)
        self.thread.start()
        
    def set_pixmap(self, data: np.ndarray):
        image = QtGui.QImage(data.data, w, h, QtGui.QImage.Format.Format_RGBA8888)
        pixmap = QtGui.QPixmap.fromImage(image)
        self.label.setPixmap(pixmap)
        
window = Widget()  

#  窗口控件的设置
window.setWindowTitle("Pyside6 GU基本结构")
window.resize(500, 500)  # 设置尺寸

# 展示窗口界面
window.show()
# 开始执行应用程序,并进入事件循环  app.exec()
sys.exit(app.exec())   #  sys.exit()  应用程序结束,状态码为0(用于收集应用程序状态码,并关闭主程序),
用python实现快速泊松盘采样