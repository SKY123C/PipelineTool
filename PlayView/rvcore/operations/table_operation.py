import pathlib
import cv2
import threading
from PySide6 import QtGui, QtCore
import time
from rvcore import utl
import os
from datetime import datetime
import subprocess
import enum
import logging

log = logging.getLogger("RVPlayView")


class CaptureStatus(enum.Enum):
    START = 0
    FINISHED = 1
    
class TableOperation(QtCore.QObject):


    class CaptureStatus(enum.Enum):
        START = 0
        FINISHED = 1
    
    capture_frame_finished = QtCore.Signal()
    single_frame_finished = QtCore.Signal(str, str)
    capture_video_status = QtCore.Signal(type(CaptureStatus.START))
    def __init__(self) -> None:
        super().__init__()
        self.image_size = [740,480]
    
    def video_to_frame(self, video_list, callback=None):
        thread = threading.Thread(target=self.video_to_frame_impl, args=(video_list,))
        thread.start()
        
    def video_to_frame_impl(self, video_list):
        a = time.time()
        ffmpeg_path = pathlib.Path(__file__).parent.parent.parent.joinpath("lib/site-packages/bin/ffmpeg.exe").as_posix()
        for video in video_list:
            save_image_path = utl.PathData.temp_image_path(video)
            if os.path.exists(save_image_path):
                self.single_frame_finished.emit(os.path.basename(video), save_image_path)
                continue
            if video.split(".")[-1].lower() in utl.get_support_image_type():
                if os.path.exists(video):
                    image_path = video
                else:
                    dir_name = os.path.dirname(video)
                    image_list = utl.listDir(dir_name)
                    image_path = os.path.join(dir_name, image_list[1] if len(image_list) > 1 else image_list[0])
                try:
                    image = cv2.imread(image_path)
                    frame = cv2.resize(image, self.image_size)
                    retval = cv2.imwrite(save_image_path, frame)
                    if retval:
                        self.single_frame_finished.emit(os.path.basename(video), save_image_path)
                except Exception as e:
                    log.error(image_path)
                    
            else:
                if os.path.isdir(video):
                    continue
                if not os.path.exists(video):
                    self.single_frame_finished.emit(os.path.basename(video), save_image_path)
                    continue
                video_obj = cv2.VideoCapture(video)
                second = 1
                while True:
                    if second > 1 :
                        res, image = video_obj.read()
                        if res:
                            frame = cv2.resize(image, self.image_size)
                            cv2.imwrite(save_image_path, frame)
                        else:
                            cmd = rf'{ffmpeg_path} -i {video} -frames:v 1 -vf "scale={self.image_size[0]}:{self.image_size[1]}:force_original_aspect_ratio=decrease" {save_image_path}'
                            subprocess.Popen(cmd, shell=True,stdout=subprocess.DEVNULL, stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        self.single_frame_finished.emit(os.path.basename(video), save_image_path)
                        break
                    second += 1
        b = time.time()
        log.warning(f"Capturing images takes time: {b-a}",)
        self.capture_frame_finished.emit()
        
    def convert_frame_to_image(self, frame_info: utl.TableFrameInfo, callback):
        thread = threading.Thread(target=self.convert_frame_to_image_impl, args=(frame_info, callback))
        thread.start()
    
    def convert_frame_to_image_impl(self, frame_info: utl.TableFrameInfo, callback, is_copy_video=False):
        self.capture_video_status.emit(CaptureStatus.START)
        video_path = frame_info.mouse_at_modex.data()
        video_path = video_path.split("|")[0]
        image_list = []
        a = time.time()
        #video_path = r"E:\ISL0020_ANI_v015.mov"
        if video_path.split(".")[-1].lower() in utl.get_support_image_type():
            ...
        else:
            video_obj = cv2.VideoCapture(video_path)
            while True:
                result, frame = video_obj.read()
                if not result:
                    break
                image_list.append(QtGui.QImage(frame.data, frame.shape[1], frame.shape[0], frame.strides[0], QtGui.QImage.Format.Format_RGB888))
        log.warning(f"Obtaining all video frames takes time: {time.time()-a}",)
        if image_list:
            frame_info.frame_image_list = image_list
            self.capture_video_status.emit(CaptureStatus.FINISHED)
            callback(frame_info)
    
    # def toQImage(im, copy=False):
    #     if im is None:
    #         return QtGui.QImage()

    #     if im.dtype == np.uint8:
    #         if len(im.shape) == 2:
    #             qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_Indexed8)
    #             qim.setColorTable(gray_color_table)
    #             return qim.copy() if copy else qim

    #         elif len(im.shape) == 3:
    #             if im.shape[2] == 3:
    #                 qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_RGB888);
    #                 return qim.copy() if copy else qim
    #             elif im.shape[2] == 4:
    #                 qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_ARGB32);
    #                 return qim.copy() if copy else qim
    
    def check_item(self, rule_dict, item_data_list: list[utl.ItemData]):
        
        for item_data in item_data_list:
            ...
            result = []
            for rule, value_list in rule_dict.items():
                item_sign_value_list = getattr(item_data, f"get_{rule}")()
                if not item_sign_value_list:
                    continue
                if not value_list:
                    if rule != "task_last_submit_time":
                        result.append(False)
                    else:
                        result.append(True)
                else:
                    for value in value_list:
                        temp_result = []
                        for item_value in item_sign_value_list:
                            if rule != "task_last_submit_time":
                                temp_result.append(True if value in item_value else False)
                            else:
                                item_time = datetime.strptime(item_value, '%Y-%m-%d %H:%M:%S')
                                for time_value in value_list:
                                    temp_result.append(True if item_time >= time_value[0] and item_time <= time_value[1] else False)
                            #temp_result.append(True if value in item_value else False)
                        if temp_result and any(temp_result):
                            result.append(True)
                            break
                    else:
                        result.append(False)
                
                if result and not all(result):
                    break
            if all(result):
                item_data.set_render_state(True)
            else:
                item_data.set_render_state(False)
    
    def get_cloud_version_data_dict(self, item_data: utl.ItemData):
        path = item_data.get_file(is_package=True).split("|")[0]
        version_path = os.path.dirname(os.path.dirname(path))
        '''暂时不支持云端的多任务，原因是云端文件夹不规范'''
        #task_entity_path = os.path.dirname(version_path)
        task_entity = os.path.basename(version_path)
        result = []
        data_dict = {task_entity: result}
        for i in os.listdir(version_path):
            result.append({"path": os.path.join(version_path, i), "entity": i})
        return data_dict
    
    def get_all_video_list(self, result):
        video_list = []
        for i in result:
            for j in i:
                if isinstance(j, list):
                    video_list.extend([item.get_file(is_package=True) for item in j if item.get_file(is_package=True)])
                else:
                    if j.get_file():
                        video_list.append(j.get_file(is_package=True))
        return video_list