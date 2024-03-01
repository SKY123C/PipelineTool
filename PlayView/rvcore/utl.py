import cgtw2
import enum
import pathlib
import time
from dataclasses import dataclass, field
from PySide6 import QtCore, QtGui
import os
from rvcore.network import rvNetwork
import json
import subprocess
import re
import functools
import configparser
from datetime import datetime


@dataclass
class TableFrameInfo:
    mouse_at_modex: QtCore.QModelIndex
    image_index_in_video: int = -1
    frame_image_list: list = field(default_factory=list)
    frame_map: dict = field(default_factory=dict)
    def get_current_pixmap(self, option):
        pixmap = None
        if not self.is_init_finished():
            return pixmap
        if self.image_index_in_video in self.frame_map:
            pixmap = self.frame_map.get(self.image_index_in_video)
        else:
            image = self.frame_image_list[self.image_index_in_video]
            pixmap = QtGui.QPixmap.fromImage(image.scaled(option.rect.size()))
        return pixmap
    
    def is_init_finished(self):
        if self.frame_image_list:
            return True


class TWItemData:
    def __init__(self, data_dict, cloud):
        self.is_in_tw = cloud
        self.generate_property(data_dict)
        
    def generate_property(self, data_dict):
        self.update(data_dict)
        self.__post_init__()
    
    def update(self, data_dict):
        for key, value in data_dict.items():
            setattr(self, key.replace(".", "_"), value)
    
    def __post_init__(self):
        if not self.task_last_submit_time:
            self.task_last_submit_time = "1111-11-11 11:11:11"
    
    def get_cloud_state(self):
        return self.is_in_tw
    
            
class ItemData:
    def __init__(self, data_dict_list, cloud):
        self.__items = []
        self.__render_state = True
        self.__sign_list = []
        self.generate_property(data_dict_list, cloud)
    
    def generate_property(self, data_dict_list, cloud):
        keys = set()
        for data_dict in data_dict_list:
            self.__items.append(TWItemData(data_dict, cloud))
            for key, values in data_dict.items():
                keys.add(key.replace(".", "_"))
        for func_name in keys:
            setattr(self, f"get_{func_name}", self.__dynamic_func(func_name))
        self.__sign_list = list(keys)
    
    def get_signs(self):
        return self.__sign_list
    
    def export(self):
        result = {}
        item = self.__items[0]
        for sign in self.__sign_list:
            result[sign] = getattr(item, f"{sign}")
        return result
    
    def __dynamic_func(self, attr_name):
        new_func = functools.partial(self.__get_result, sign=attr_name)
        return new_func
    
    def __get_result(self, sign, is_package=False, repeat=False):
        result = []
        for i in self.__items:
            value = getattr(i, sign)
            if repeat and value in result:
                continue
            if value:
                result.append(value)
        if is_package:
            result_str = ""
            for i in result:
                result_str += str(i)
                result_str += "|"
            return result_str[0:-1]
        return result
    
    def is_in_cloud(self):
        for i in self.__items:
            return i.is_in_tw
    
    def update_cloud(self, data_dict, is_update=True):
        for i in self.__items:
            if is_update:
                i.is_in_tw = not i.is_in_tw
            i.update(data_dict)
            
    def set_render_state(self, result):
        self.__render_state = result
        
    def get_render_state(self):
        return self.__render_state

    def get_tool_tip(self):
        time = self.get_task_last_submit_time(is_package=True, repeat=True)
        art = self.get_task_account(is_package=True)
        status = self.get_task_task_leader_status(is_package=True)
        file = self.get_file(is_package=True)
        #art = art if art else self.get_create_by(is_package=True)
        return f"最后提交时间：{time}\n制作人员：{art}\n审核状态：{status}\n文件路径：{file}"
    
    def get_all_tw_data(self):
        return self.__items
        
        
class TWSign:
    def __init__(self, sign, label="", display_state=True, default_value=""):
        self.sign = sign
        self.label = label
        self.default_value = default_value
        self.display_state = display_state
    
    def get_sign(self):
        return self.sign
    
    def get_label(self):
        return self.label
    
    def set_label(self, label):
        self.label = label
    
    def get_display_state(self):
        return self.display_state
    
    def get_default_value(self):
        return self.default_value
        
        
class PathData:
    thumbnail_root_path = pathlib.Path(r"\\10.236.200.20\UE_Lib\tools\TA\RVTool\thumbnail")
    @classmethod
    def temp_image_path(cls, video_path):
        result = video_path.rsplit("CGteamwork", 1)
        result = cls.thumbnail_root_path.joinpath(result[-1].lstrip("/").lstrip("\\")).with_suffix(".jpg")
        if not result.parent.exists():
            result.parent.mkdir(parents=True, exist_ok=True)
        return str(result)
    
    @classmethod
    def get_ini_path(cls):
        file_path = pathlib.Path(__file__).parent.parent.joinpath("RVPlayView.ini")
        return file_path

class TWLib:
    instance = None
    
    class ModuleType(enum.IntEnum):
        INFO = 0
        TASK = 1
    
    def get_sign_list(self):
        return self.__sign_list
    
    def init(self):
        self.__sign_list: list[TWSign] = []
        ["shot.entity", "pipeline.entity", "task.last_submit_time", "task.entity", "task.task_leader_status", "task.account", "task.id", "ani.entity", "task.artist"]
        
        self.__sign_list.append(TWSign("shot.entity"))
        self.__sign_list.append(TWSign("pipeline.entity"))
        self.__sign_list.append(TWSign("task.last_submit_time", display_state=False, default_value="1111-11-11 11:11:11"))
        self.__sign_list.append(TWSign("task.task_leader_status"))
        self.__sign_list.append(TWSign("task.account", display_state=False))
        self.__sign_list.append(TWSign("task.id", display_state=False))
        self.__sign_list.append(TWSign("ani.entity"))
        self.__sign_list.append(TWSign("task.artist"))
        self.__sign_list.append(TWSign("task.entity"))
        self.__sign_list.append(TWSign("shot.status"))
        result = self.tw.task.fields_and_str("proj_iii", "shot")
        for j in result:
            for i in self.__sign_list:
                if i.get_sign() == j.get("sign"):
                    i.set_label(j.get("field_str"))
                    break
        
    def get_status_color(self, status):
        if not status:
            return "#FFFFFF"
        return self.__color_map.get(status)
    
    def get_status(self):
        return self.__color_map
    
    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            tw = cgtw2.tw()
            obj = super().__new__(cls)
            cls.instance = obj
            obj.tw = tw
            obj.__color_map = obj.tw.status.get_status_and_color()
            obj.init()
        return cls.instance
    
    def get_all_project(self, db_entity=None, bGet=False):
        t_id_list =  self.tw.info.get_id(db='public', module='project', filter_list=[])
        info_list = self.tw.info.get(db='public', module='project', id_list=t_id_list, field_sign_list=['project.entity','project.database'], order_sign_list=["project.entity"])
        result = {"info_list": info_list}
        if bGet and db_entity is not None:
            db = [i.get('project.database') for i in info_list if i.get('project.entity') == db_entity]
            result["db"] = db[0] if db else None
        return result
    
    def get_db(self, db_entity=None, bGet=False):
        all_db_info = self.get_all_project(db_entity, True)
        db = all_db_info.get("db")
        return db
    
    def get_info(self, db_entity, module, module_type, filter_list, sign, order_sign_list):
        db = self.get_db(db_entity, True)
        interface = self.tw.task if module_type == TWLib.ModuleType.TASK else self.tw.info
        id_list = interface.get_id(db, module, filter_list)
        result = interface.get(db, module, id_list, sign, order_sign_list=order_sign_list)
        for i in result:
            i["db_entity"] = db_entity
        return result

    def get_task_sign_list(self):
        result = [i.get_sign() for i in self.__sign_list]
        return result
    
    def get_latest_shot_video(self, db_entity, filter_list, stage_sort_list):
        a = time.time()
        new_result = self.__create_item_data_by_tw_data(db_entity, filter_list, stage_sort_list)
        cloud_stage = get_cloud_stage()
        parent_path = get_cloud_path()
        for item_list in new_result:
            for item in item_list:
                abs_item = item[0] if isinstance(item, list) else item
                if abs_item.get_pipeline_entity(is_package=True) in cloud_stage:
                    self.__update_cloud_data(parent_path, abs_item)
                        
        b = time.time()
        print("获取全部镜头数据")
        print(b-a)
        return new_result
    
    def __create_item_data_by_tw_data(self, db_entity, filter_list, stage_sort_list):
        db = self.get_db(db_entity, True)
        #id_list = self.tw.task.get_id(db, "shot", filter_list)
        shot_info_list = self.get_info(db_entity, "shot", TWLib.ModuleType.TASK, filter_list, self.get_task_sign_list(), ["shot.entity"])
        id_list = [i.get("task.id") for i in shot_info_list]
        #shot_info_list = self.tw.task.get(db, "shot", id_list,field_sign_list=self.get_task_sign_list(), order_sign_list=["shot.entity"])
        file_list = self.tw.task.get_review_file(db, "shot", id_list)
        result = []
        last_shot_entity = None
        for i in shot_info_list:
            if not last_shot_entity:
                result.append([i])
            else:
                if i.get("shot.entity") != last_shot_entity:
                    result.append([i])
                else:
                    result[-1].append(i)
            for file_index, j in enumerate(file_list):
                video_file = j.get("path")[0]
                if i.get("shot.entity") in video_file and i.get("task.entity") in video_file:
                    i["file"] = video_file
                    file_list.pop(file_index)
                    break
            else:
                i["file"] = None
            last_shot_entity = i.get("shot.entity")
        new_result = []
        
        #根据阶段列表排序
        for i in result:
            new_result.append([])
            for index, stage in enumerate(stage_sort_list):
                saved_stage = []
                for j in i:
                    if stage.lower() == j.get("pipeline.entity").lower():
                        if stage not in saved_stage:
                            new_result[-1].append(self.__create_item_data([j]))
                            saved_stage.append(stage)
                        else:
                            if isinstance(new_result[-1][-1], list):
                                new_result[-1][-1].append(self.__create_item_data([j]))
                            else:
                                data = new_result[-1][-1]
                                new_result[-1][-1] = [data, self.__create_item_data([j])]
                
                if not saved_stage:
                    new_result[-1].append(self.__create_item_data([self.__get_default_item_data_dict(
                                                                    {
                                                                    "db_entity": i[0].get("db_entity"),
                                                                    "pipeline.entity": stage, 
                                                                    "file": None, 
                                                                    "shot.entity": i[0].get("shot.entity"), 
                                                                    "task.entity": stage, 
                                                                    "ani.entity": i[0].get("ani.entity")
                                                                    }
                                                                    )
                                                                   ]))
                saved_stage.clear()
        for item_list in new_result:
            for item in item_list:
                if isinstance(item, list):
                    item.sort(reverse = True, key=lambda x: datetime.strptime(x.get_task_last_submit_time(is_package=True), '%Y-%m-%d %H:%M:%S'))
        return new_result
        ...
    def __get_default_item_data_dict(self, default_data_dict):
        result = {}
        for i in self.__sign_list:
            result[i.get_sign()] =i.get_default_value()
        result.update(default_data_dict)
        return result
        ...
        
    def get_item_data_by_cloud_state(self, db_entity, item_data: ItemData):
        
        b_cloud = item_data.is_in_cloud()
        shot_entity = item_data.get_shot_entity()[0]
        pipeline_entity = item_data.get_pipeline_entity()[0]
        ani_entity = item_data.get_ani_entity()[0]
        new_result = self.__create_item_data_by_tw_data(db_entity, [["shot.entity", "=", shot_entity], "and",
                                                ["pipeline.entity", "=", pipeline_entity], "and",
                                                ["ani.entity", "=", ani_entity]], [pipeline_entity])
        if not b_cloud:
            cloud_stage = get_cloud_stage()
            parent_path = get_cloud_path()
            for item_list in new_result:
                for item in item_list:
                    abs_item = item[0] if isinstance(item, list) else item
                    if abs_item.get_pipeline_entity(is_package=True) in cloud_stage:
                        self.__update_cloud_data(parent_path, abs_item, is_compare=False)
            
        return new_result
        ...
    def __update_cloud_data(self, parent_path, abs_item, is_compare=True, is_update_state=True):
        latest_info = get_latest_clound_info(parent_path, abs_item.get_ani_entity(is_package=True),
                            abs_item.get_shot_entity(is_package=True),
                            abs_item.get_task_entity(is_package=True))
        if latest_info:
            latest_time = latest_info.get("time")
            path = latest_info.get("path")
            path = str(path)
            item_time = datetime.strptime(abs_item.get_task_last_submit_time(is_package=True), '%Y-%m-%d %H:%M:%S')
            if is_compare:
                if item_time < latest_time:
                    abs_item.update_cloud({"file": path, "task.last_submit_time": latest_time.strftime('%Y-%m-%d %H:%M:%S')}, is_update_state)
            else:
                abs_item.update_cloud({"file": path, "task.last_submit_time": latest_time.strftime('%Y-%m-%d %H:%M:%S')}, is_update_state)
    
    def __create_item_data(self, data_dict_list: list, cloud=False):
        return ItemData(data_dict_list, cloud)
    
    def __create_cloud_item_data(self, item_data):
        ...
    
    def jump_teamwork(self, db_entity, task_id, module, module_type):
        ip = self.tw.login.http_server_ip()
        self.tw.send_local_socket("main_widget", "activate_window", {}, "send")
        all_db_info = self.get_all_project(db_entity, True)
        db = all_db_info.get("db")
        token = self.tw.login.token()
        lang=self.tw.send_local_socket("main_widget", "get_client_language", {}, "get")
        theme=self.tw.send_local_socket("main_widget", "get_client_theme", {}, "get")
        t_url="https://"+ip+"/index.php?controller=v_main_window&method=show_page&db="+db+"&code="+db+"&module="+module+"&module_type="+module_type+"&is_qt=y&token="+token+"&lang="+lang+"&theme="+theme
        t_dic={"url":t_url, "key":db, "text":"Big", "cookie_data":task_id}
        self.tw.send_local_socket("main_widget", "create_project_widget", t_dic, "send")
    

    def get_same_stage_shot_info(self, db_entity, session, shot_entity, stage, item_type=None):
        shot_info_list = self.get_info(db_entity, "shot", TWLib.ModuleType.TASK, [["ani.entity_concat", "=", session], "and",
                                                            ["pipeline.entity", "=", stage], "and",
                                                            ["shot.entity", "=", shot_entity]], ["task.entity"], [])
        db = self.get_db(db_entity, True)
        result = {}
        for item_info in shot_info_list:
            task_entity = item_info.get("task.entity")
            if not task_entity:
                continue
            t_version_id_list =  self.tw.version.get_id(db=db, filter_list=[['module','=','shot'],'and',['module_type','=','task'],'and',['#link_id','=',item_info.get('id')], 'and', ['sign', '=', 'review']])
            version_list = self.tw.version.get(db, t_version_id_list, ['entity', 'create_time', 'link_entity', "#link_id", "create_by"], order_list=['entity'])
            result[task_entity] = version_list
        return result
        
    def get_item_data_by_version(self, db_entity, verion_info_list, src_item_data):
        data_dict_list = []
        support_video_type = get_support_video_type()
        db = self.get_db(db_entity, True)
        for version_info in verion_info_list:
            if version_info.get("path"):
                data_dict = src_item_data.export()
                info = get_latest_clound_info_by_path(version_info.get("path"))
                data_dict["file"] = str(info.get("path"))
                data_dict["task_submit_time"] = info.get("time")
                data_dict_list.append(data_dict)
            else:
                file_id = self.tw.file.get_id(db, [["#version_id", "=", version_info.get("version_id")]])
                file_info = self.tw.file.get(db, file_id, ["sys_local_full_path", "sys_create_by"])
                file_list = [i.get("sys_local_full_path") for i in file_info if i.get("sys_local_full_path").split(".")[-1].lower() in support_video_type]
                shot_info_list = self.tw.task.get(db, "shot", [version_info.get("task_id")],field_sign_list=self.get_task_sign_list(), order_sign_list=["shot.entity"])
                if shot_info_list:
                    shot_info_list[0]["file"] = file_list[0] if file_list else None
                    shot_info_list[0]["task.account"] = file_info[0].get("sys_create_by")
                    shot_info_list[0]["db_entity"] = db_entity
                    data_dict_list.append(shot_info_list[0])
        
        item_data = self.__create_item_data(data_dict_list, src_item_data.is_in_cloud())
        return item_data

    def get_software_path(self, db_entity, name):
        db = self.get_db(db_entity, True)
        path = self.tw.software.get_path(db, name)
        return path

    def get_all_session(self):
        result = []
        id_list = self.tw.project.get_id([["project.status", "=", "Active"]])
        project_list = self.tw.project.get(id_list, ["project.entity", "project.database"], order_sign_list=["project.entity"])
        for project_info in project_list:
            entity = project_info.get("project.entity")
            db = project_info.get("project.database")
            #["ani.finished_degree", "!=", "Finished"]
            #id_list = self.tw.info.get_id(db, "ani", [["ani.finished_degree", "!=", "Finished"]])
            id_list = self.tw.info.get_id(db, "ani", [])
            data = self.tw.info.get(db, "ani", id_list, ["ani.entity_concat"], order_sign_list=["ani.entity_concat"])
            data_dict = {entity:data}
            result.append(data_dict)
        return result
        
def get_support_video_type():
    image_type = get_support_image_type()
    video_type = ["mp4", "mov"]
    video_type.extend(image_type)
    return video_type

def get_support_image_type():
    return ["jpg", "png", "tif"]

def get_cloud_stage():
    return ["CMP", "RCL", "PKG"]

def get_cloun_root_path():
    return pathlib.Path(r"\\10.236.200.22/")

def get_cloud_path():
    return get_cloun_root_path().joinpath("VEoutput").resolve()

def get_latest_clound_info(parent_path: pathlib.Path, ani_entity, shot_entity, task_entity):
    dst_path = parent_path.joinpath(ani_entity, shot_entity, task_entity)
    info = {}
    if not dst_path.exists():
        return
    result = []
    for p in dst_path.iterdir():
        if not p.is_dir():
            continue
        result.append(p)
    if result:
        result.sort(key=lambda x:x.lstat().st_mtime)
        info["time"] = datetime.fromtimestamp(result[-1].lstat().st_mtime)
        info["path"] = get_sequence_string(result[-1])
        return info

def get_latest_clound_info_by_path(path):
    path = pathlib.Path(path)
    info = {}
    info["time"] = datetime.fromtimestamp(path.lstat().st_mtime)
    info["path"] = get_sequence_string(path)
    return info
        
def rvCmd(playMode, files, values, path, port):
    RVEXIT = 0
    if playMode not in ["defaultSequence", "defaultLayout"]:
        return 
    if not files:
        return
    port = port
    files = json.dumps(files).replace('[', '{').replace(']', '}').replace('(', '{').replace(')', '}')
    values = json.dumps(values).replace('[', '{').replace(']', '}').replace('(', '{').replace(')', '}')
    rvc = rvNetwork.RvCommunicator("AddSource")
    cmd = '"%s" -network -networkPort %d' % (path, port) 
    args = ' -view %s' % playMode
    a = subprocess.Popen(cmd + args)
    while not rvc.connected:
        rvc.connect("127.0.0.1", port)
    cmd = (
        """
    {
        int _ret = 0;
        clearSession();
        string[][][] fileNames_list = %s;
        string[][][][] values_list = %s;
        string[] RVSequenceNodes;
        RVSequenceNodes.resize(fileNames_list.size());
        for (int i=0; i<fileNames_list.size();i++)
        {
            string[] RVSources = addSourcesVerbose(fileNames_list[i]);
            string[] RVSourcesGroups;
            RVSourcesGroups.resize(RVSources.size());
            for (int j=0;j < RVSources.size();j++)
            {
                string SourceName = RVSources[j];
                string[][] attrs = values_list[i][j];
                for (int AttrIndex=0;AttrIndex < attrs.size();AttrIndex++)
                {
                    string AttributeName = SourceName + ".attributes.comment_" + attrs[AttrIndex][0];
                    string AttributeValue = attrs[AttrIndex][1];
                    newProperty(AttributeName, StringType, 1);
                    setStringProperty(AttributeName, string[] {AttributeValue}, true);
                }
                string RVSourceGroup = nodeGroup(SourceName);
                RVSourcesGroups[j] = string(RVSourceGroup);
            }
            string RVSequenceNode = newNode("RVSequenceGroup");
            RVSequenceNodes[i] = string(RVSequenceNode);
            setNodeInputs(RVSequenceNode, RVSourcesGroups);
        }

        string RVLayoutNode = newNode("RVLayoutGroup");
        setNodeInputs(RVLayoutNode, RVSequenceNodes);
        setViewNode(RVLayoutNode);

    }
        """
        % (files, values)
    )
    rvc.remoteEvalAndReturn(cmd)
    rvc.disconnect()

def listDir(path: pathlib.Path):
    if isinstance(path, str):
        return [i for i in os.listdir(path) if i != 'Thumbs.db' and i.split(".")[-1] not in ["mp4", "mov"]]
    else:
        return [i for i in path.iterdir() if i.name != 'Thumbs.db' and i.suffix.lower() not in [".mp4", ".mov"]]

def splitFileSequence(first_file_path: pathlib.Path, last_file_path: pathlib.Path):
    firstFile = first_file_path.name
    lastFile = last_file_path.name
    first_digit = re.findall(r'\d+', firstFile)
    last_digit = re.findall(r'\d+', lastFile)
    result = [i for i in zip(first_digit, last_digit) if i[0] != i[1]][0]
    rule_str, frame = (firstFile, result[0])if firstFile.count(result[0]) <= 1 else (lastFile, result[1])
    start_index = rule_str.find(frame)
    src_list = list(rule_str)
    if result.index(frame):
        src_list.insert(start_index + len(frame), '#')
        src_list.insert(start_index, result[0] + '-')
    else:
        src_list.insert(start_index + len(frame), '-' + result[-1] + '#')
    sequenceFrame = ''.join(src_list)
    return sequenceFrame

def get_sequence_string(path: pathlib.Path):
    file_list = listDir(path)
    if len(file_list) > 1:
        file_name = splitFileSequence(file_list[0], file_list[-1])
    elif len(file_list) == 1:
        file_name = file_list[0]
    else:
        file_name = ""
    return path.joinpath(file_name).resolve()
    return os.path.join(path, file_name)



def get_saved_sessions_from_init():
    config = configparser.ConfigParser()
    file_path = PathData.get_ini_path()
    config.read(file_path, encoding="utf-8")
    sections = config.sections()
    result = []
    if "Setting" in sections:
        result = config["Setting"]["Sessions"]
    return result

def get_main_net_port():
    port = 32145
    return port

def convert_unc_path(path):
    new_path = path.replace(r"\\", "\\")
    
    
    ...