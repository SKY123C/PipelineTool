from typing import Optional, Union
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import QModelIndex, QPersistentModelIndex
from PySide6.QtGui import QHelpEvent, QResizeEvent
from PySide6.QtWidgets import QAbstractItemView, QStyleOptionViewItem, QWidget
from rv_widgets import rv_utl_widgets, rv_filter_widget
from rv_widgets.rv_actions import play_action
from rvcore import event_manager, utl, menu_manager
from rvcore.base_classes import base_action, base_table
from rvcore.operations import table_operation
import os
import re
from datetime import datetime, timedelta
import random
from enum import Enum


class RVTableModel(QtCore.QAbstractTableModel):
    database_filename = QtCore.Property(str)
    def __init__(self):
        super().__init__()
        self.__stage_list = ['LAY', 'ANI', 'CFX', 'EFX', 'SET', 'LGT', 'CMP', 'RCL', 'PKG']
        self.__tool_list = ["最新视频"]
        self.__source_data = []
        self.header_init()
        self.share_brush = QtGui.QBrush(QtGui.QColor(193, 193, 193))
    
    @property
    def stage_list(self):
        return self.__stage_list
    
    @property
    def source_data(self):
        return self.__source_data
    
    def set_init_data(self, data_list):
        self.__source_data = data_list
        ...
    
    def update_date(self, index: QtCore.QModelIndex, item_data):
        self.__source_data[index.row()][index.column()] = item_data
        ...
    
    def __get_last_source_data(self, row):
        item_list = []
        
        for item in self.__source_data[row]:
            child_item = item[0] if isinstance(item, list) else item
            if child_item.get_file(is_package=True):
                item_list.append(child_item)
        return item_list[-1] if item_list else child_item
        ...
    def data(self, idx: QtCore.QModelIndex, role: int = ...) :
        if idx.column() >=0 and idx.row() >= 0:
            if idx.column() >= len(self.__stage_list):
                child_item = self.__get_last_source_data(idx.row())
            else:
                item = self.__source_data[idx.row()][idx.column()]
                child_item = item[0] if isinstance(item, list) else item
            if role == QtCore.Qt.ItemDataRole.DisplayRole:
                return child_item.get_file(is_package=True)
            if role == QtCore.Qt.ItemDataRole.UserRole:
                return child_item
            if role == QtCore.Qt.ItemDataRole.ToolTipRole:
                return child_item.get_tool_tip()
            if role == QtCore.Qt.ItemDataRole.BackgroundRole:
                return self.share_brush
        
    def rowCount(self, parent: QtCore.QModelIndex=None) -> int:
        return len(self.__source_data)
    
    def columnCount(self, parent: QtCore.QModelIndex=None) -> int:
        return len(self.__stage_list) + len(self.__tool_list)

    def header_init(self):
        for index, stage in enumerate(self.__stage_list + self.__tool_list):
            self.setHeaderData(index, QtCore.Qt.Orientation.Horizontal, stage)
    
    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = ...):
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            if orientation == QtCore.Qt.Orientation.Horizontal:
                return self.__stage_list[section] if section < len(self.__stage_list) else self.__tool_list[section - len(self.__stage_list)]
            else:
                return self.__source_data[section][0].get_shot_entity(is_package=True, repeat=True)


class RVTableDelegate(QtWidgets.QStyledItemDelegate):
    
    over_time_signal = QtCore.Signal(utl.TableFrameInfo)
    request_paint = QtCore.Signal(QtCore.QRect)
    
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.pixmap_map = {}
        self.palette = QtGui.QPalette()
        self.palette.setColor(QtGui.QPalette.ColorRole.Text, QtGui.QColor(200, 200, 200))
        self.__temp_info: utl.TableFrameInfo = None
        self.__cloud_image = QtGui.QImage(r":/resources/cloud_16.png")
        self.a = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timeout)
        self.pixmap_cache_map = {}
    
    def add_cache(self, video_name, image_path):
        image = QtGui.QImage(image_path)
        #pixmap = QtGui.QPixmap.fromImage(image.scaled(option.rect.size()))
        #os.path.basename(image_path)
        self.pixmap_cache_map[video_name] = image
        ...
    
    def reset_cache(self):
        self.pixmap_cache_map.clear()
        
    def paint(self, painter: QtGui.QPainter, option: QtWidgets.QStyleOptionViewItem, index: QtCore.QModelIndex) -> None:

        self.paint_background(painter, option, index)
        data = index.data()
        item_data = index.data(QtCore.Qt.ItemDataRole.UserRole)
        if data and item_data.get_render_state():
            '''进去item rect中'''
            if option.state & QtWidgets.QStyle.StateFlag.State_MouseOver:
                if not self.__temp_info:
                    self.timer.start(3000)
                    self.__temp_info = utl.TableFrameInfo(index)
                    self.custom_paint(painter, option, index)
                else:
                    if self.__temp_info.mouse_at_modex == index:
                        self.custom_paint_frame(painter, option, self.__temp_info, index)
                    else:
                        self.timer.start(3000)
                        self.__temp_info = utl.TableFrameInfo(index)
                        self.custom_paint(painter, option, index)
            else:
                if self.__temp_info and index == self.__temp_info.mouse_at_modex:
                    self.__temp_info = None
                self.custom_paint(painter, option, index)

    def paint_background(self, painter: QtGui.QPainter, option: QtWidgets.QStyleOptionViewItem, index: QtCore.QModelIndex):
        painter.save()
        if option.state & QtWidgets.QStyle.StateFlag.State_HasFocus or option.state & QtWidgets.QStyle.StateFlag.State_Selected:
            painter.fillRect(option.rect, QtGui.QColor(191, 216, 249))
        else:
            painter.fillRect(option.rect, index.data(QtCore.Qt.ItemDataRole.BackgroundRole))
        painter.restore()

    def timeout(self):
        if self.__temp_info:
            self.over_time_signal.emit(self.__temp_info)
        self.timer.stop()
            
    def custom_paint_frame(self, painter, option, info: utl.TableFrameInfo, index):
        pixmap = info.get_current_pixmap(option)
        if pixmap:
            self.paint_image(painter, option, pixmap, index)
        else:
            self.custom_paint(painter, option, index)
        
    def custom_paint(self, painter, option, index):
        data = index.data()
        video_path = data.split("|")[-1]
        pixmap = None
        # image_path = utl.PathData.temp_image_path(video_path)
        # if not os.path.exists(image_path):
        #     return
        
        #image = QtGui.QImage(image_path)
        #pixmap = QtGui.QPixmap.fromImage(image.scaled(option.rect.size()))
        base_name = os.path.basename(video_path)
        if base_name in self.pixmap_cache_map:
            image = self.pixmap_cache_map.get(base_name)
            pixmap = QtGui.QPixmap.fromImage(image.scaled(option.rect.size()))
            #pixmap = self.pixmap_map.get(video_path)
        # else:
        #     image_path = utl.PathData.temp_image_path(video_path)
        #     if os.path.exists(image_path):
        #         image = QtGui.QImage(image_path)
        #         pixmap = QtGui.QPixmap.fromImage(image.scaled(option.rect.size()))
        #         self.pixmap_map[video_path] = pixmap
        if pixmap:
            self.paint_image(painter, option, pixmap, index)

    def paint_image(self, painter, option, pixmap, index):
        
        image_rect = self.get_image_video_rect(option)
        QtWidgets.QApplication.style().drawItemPixmap(painter, image_rect, QtCore.Qt.AlignmentFlag.AlignTop, pixmap)
        self.paint_text(painter, option, index)
        
    def paint_text(self, painter: QtGui.QPainter, option, index):
        path = index.data()
        interface = utl.TWLib()
        item_data: utl.ItemData = index.data(QtCore.Qt.ItemDataRole.UserRole)
        status = item_data.get_task_task_leader_status()
        color_str = interface.get_status_color(status[0])
        path_list = path.split("|")
        result = ""
        for i in path_list:
            result += os.path.basename(i)
            result += "|"
        color = QtGui.QColor(color_str)
        painter.setFont(QtGui.QFont("SimHei", 12))
        self.palette.setColor(QtGui.QPalette.ColorRole.Text, color)
        
        QtWidgets.QApplication.style().drawItemText(painter, option.rect, 
                                                    QtCore.Qt.AlignmentFlag.AlignBottom | QtCore.Qt.AlignmentFlag.AlignCenter, 
                                                    self.palette, True, result[0:-1], 
                                                    QtGui.QPalette.ColorRole.Text)
        if item_data.is_in_cloud():
            pixmap = QtGui.QPixmap.fromImage(self.__cloud_image.scaled(16,16))
            QtWidgets.QApplication.style().drawItemPixmap(painter, option.rect, QtCore.Qt.AlignmentFlag.AlignBottom | QtCore.Qt.AlignmentFlag.AlignLeft, pixmap)
        
    def get_image_video_rect(self, option):
        rect = QtCore.QRect(option.rect)
        rect.setHeight(option.rect.height() - 15)
        return rect
    
    def get_text_rect(self, option):
        rect = QtCore.QRect(option.rect)
        image_rect = self.get_image_video_rect(option)
        image_height = image_rect.height()
        text_y = rect.y() + image_height
        rect.setY(text_y)
        return rect
    
    def editorEvent(self, event: QtGui.QMouseEvent, model, option, index) -> bool:
        if self.__temp_info and index.column() >= 0 and index.row() >= 0:
            if event.type() == QtCore.QEvent.Type.MouseMove and self.__temp_info:
                if event.type() == QtCore.QEvent.Type.MouseMove and self.__temp_info.is_init_finished():
                    scale = event.position().x() / (option.rect.left() + option.rect.width())
                    self.__temp_info.image_index_in_video = int(scale * (len(self.__temp_info.frame_image_list) - 1))
                    self.request_paint.emit(option.rect)
                
        return super().editorEvent(event, model, option, index)

    def set_frame_info(self, frame_info: utl.TableFrameInfo):
        if self.__temp_info and frame_info.mouse_at_modex == self.__temp_info.mouse_at_modex:
            self.__temp_info = frame_info

    
class RVTable(base_table.RVTable):
    
    captured = QtCore.Signal(dict)
    data_finished = QtCore.Signal(list)
    
    def __init__(self, session, db_entity, status_bar, parent=None) -> None:
        super().__init__(base_table.TableType.TABLE, parent)
        self.opertation = table_operation.TableOperation()
        self.status_bar = status_bar
        self.session = session
        self.db_entity = db_entity
        self.data_finished.connect(lambda x:...)
        self.setModel(RVTableModel())
        self.setItemDelegate(RVTableDelegate())
        self.init()
        self.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Fixed)
        self.horizontalHeader().setDefaultSectionSize(200)
        self.verticalHeader().setDefaultSectionSize(118)
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Fixed)
    
    def init(self):
        self.filter_data = {}
        self.itemDelegate().over_time_signal.connect(self.convert_frame_to_image)
        self.itemDelegate().request_paint.connect(self.refresh)
        self.opertation.single_frame_finished.connect(self.itemDelegate().add_cache)
        self.opertation.capture_frame_finished.connect(self.refresh_all)
        self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.menu = QtWidgets.QMenu()
        menu_manager.MenuManager.get_instance().register_menu(self.session + "_TableMenu", self.menu)
        self.customContextMenuRequested.connect(self.create_menu)
        self.doubleClicked.connect(self.select_other_version)
        self.setMouseTracking(True)
    
    def set_filter_data(self, data):
        self.filter_data.update(data)
        self.opertation.check_item(self.filter_data, self.get_all_item_data())
        self.refresh_all()
        ...
    
    def get_all_item_data(self):
        row_count = self.model().rowCount()
        column_count = self.model().columnCount()
        result = []
        for row in range(row_count):
            for column in range(column_count):
                result.append(self.model().data(self.model().index(row, column), QtCore.Qt.ItemDataRole.UserRole))
        return result
        
    def setup(self):
        self.reload()
    
    def __set_shot_info(self):
        self.status_bar.update_shot(self.model().rowCount())
            
    def reload(self):
        twlib = utl.TWLib()
        result = twlib.get_latest_shot_video(self.db_entity, [["ani.entity_concat", "=", self.session], "and", 
                                                                     ["pipeline.entity", "in", self.model().stage_list]], self.model().stage_list)
        self.data_finished.emit(result)
        video_list = self.opertation.get_all_video_list(result)
        self.opertation.video_to_frame(video_list)
        self.model().beginResetModel()
        self.model().set_init_data(result)
        self.model().endResetModel()
        self.__set_shot_info()
        
    def select_other_version(self, index: QtCore.QModelIndex):
        item_data: utl.ItemData = index.data(QtCore.Qt.ItemDataRole.UserRole)
        if item_data.is_in_cloud():
            data_dict = self.opertation.get_cloud_version_data_dict(item_data)
            self.create_version_tree(data_dict)
        else:
            tw_lib = utl.TWLib()
            shot_entity = self.model().headerData(index.row(), QtCore.Qt.Orientation.Vertical, QtCore.Qt.ItemDataRole.DisplayRole)
            stage = self.model().headerData(index.column(), QtCore.Qt.Orientation.Horizontal, QtCore.Qt.ItemDataRole.DisplayRole)
            data_dict = tw_lib.get_same_stage_shot_info(self.db_entity, self.session, shot_entity, stage)
            self.create_version_tree(data_dict)
    
    def create_version_tree(self, data_dict):
        dialog = RVTableVersionDialog(data_dict)
        dialog.version_changed.connect(self.update_model)
        dialog.exec_()

    def update_model(self, info_list):
        tw_lib = utl.TWLib()
        src_item_data = self.selectedIndexes()[0].data(QtCore.Qt.ItemDataRole.UserRole)
        item_data = tw_lib.get_item_data_by_version(self.db_entity, info_list, src_item_data)
        self.opertation.video_to_frame(item_data.get_file())
        self.model().beginResetModel()
        '''添加更新图片'''
        self.model().update_date(self.selectedIndexes()[0], item_data)
        self.model().endResetModel()
        
    def get_menu_name(self):
        return self.session + "_TableMenu"
    
    def create_menu(self, pos):
        items = self.selectionModel().selectedIndexes()
        if not items:
            return
        for index in items:
            data = index.data(QtCore.Qt.ItemDataRole.UserRole)
            if not data.get_task_id():
                break
        else:
            menu_manager.MenuManager.get_instance().show_menu(self.get_menu_name(), base_action.MenuType.TABLE, 
                                                            self.mapToGlobal(pos),
                                                            index_list=items, table=self)
        
        
    def switch_path(self, index_list: list[QtCore.QModelIndex]):
        interface = utl.TWLib()
        for index in index_list:
            item_data = index.data(QtCore.Qt.ItemDataRole.UserRole)
            result = interface.get_item_data_by_cloud_state(self.db_entity, item_data)
            self.model().beginResetModel()
            self.model().update_date(index, result[0])
            self.model().endResetModel()
            ...
        ...
    def convert_frame_to_image(self, frame_info):
        #frame_info.state = True
        self.opertation.convert_frame_to_image(frame_info, self.set_delegate_image_list)

    def set_delegate_image_list(self ,frame_info):
        self.itemDelegate().set_frame_info(frame_info)
        
    def refresh(self, index: QtCore.QModelIndex):
        self.viewport().repaint(index)
    
    def refresh_all(self):
        #self.viewport().update()
        self.repaint()
        #self.model().dataChanged()
        ...
    def filter_shot(self, text):
        if '-' in text:
            self.__hideContinuousRows(text)
        else:
            self.__hideMultipleRows(text)
            
    def __hideMultipleRows(self, text):
        row_count = self.model().rowCount()
        text_list = list(set(text.split(",")))
        for row in range(row_count):
            shot_entity = self.model().headerData(row, QtCore.Qt.Orientation.Vertical, QtCore.Qt.ItemDataRole.DisplayRole)
            if any([True if every_text.lower() in shot_entity.lower() else False for every_text in text_list]):
                self.setRowHidden(row, False)
            else:
                self.setRowHidden(row, True)
    
    def __hideContinuousRows(self,text):
        row_count = self.model().rowCount()
        text_list = [i for i in text.split("-") if i]
        if 0 < len(text_list) < 3:
            start = int(text_list[0].lstrip('0'))
            if len(text_list) < 2:
                end = 1000
            else:
                end = int(text_list[1].lstrip('0'))
            range_list = list(range(start, end+1))
            for row in range(row_count):
                shot_entity = self.model().headerData(row, QtCore.Qt.Orientation.Vertical, QtCore.Qt.ItemDataRole.DisplayRole)
                itemText = re.sub("[^0-9]", "",shot_entity)
                if itemText:
                    itemText = itemText.lstrip('0')
                    if int(itemText) in range_list:
                        self.setRowHidden(row, True)
                    else:
                        self.setRowHidden(row, True)
    
    def play_selected(self):
        action = play_action.PlayAction(self.selectedIndexes(), self)
        action.trigger()
        

class RVStatusWidget(QtWidgets.QDialog):
    item_clicked = QtCore.Signal(dict)
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setup()
    
    def setup(self):
        interface = utl.TWLib()
        self.resize(200,200)
        status_dict = interface.get_status()
        self.setWindowFlags(QtCore.Qt.WindowType.Popup | QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        layout = QtWidgets.QVBoxLayout(self)
        self.list_widget = QtWidgets.QListWidget()
        for status, color_name in status_dict.items():
            item = QtWidgets.QListWidgetItem()
            item.setCheckState(QtCore.Qt.CheckState.Checked)
            item.setText(status)
            #item.setCheckState()
            item.setForeground(QtGui.QColor(color_name))
            self.list_widget.addItem(item)
        layout.addWidget(self.list_widget, 1)
        self.list_widget.itemClicked.connect(self.on_item_clicked)
    
    def on_item_clicked(self, item=None):
        #self.close()
        result = []
        for row in range(self.list_widget.count()):
            child_item = self.list_widget.item(row)
            if child_item.checkState() == QtCore.Qt.CheckState.Checked:
                result.append(child_item.text())
        self.item_clicked.emit({"task_task_leader_status": result})


class RVTableToolbar(QtWidgets.QToolBar):
    
    status_changed = QtCore.Signal(dict)
    
    class TimeEnum(Enum):
        DAY = "今天"
        WEEK = "本周"
        MONTH = "本月"
        
    def __init__(self, table: RVTable):
        super().__init__()
        self.table = table
        self.setup()
    
    def setup(self):
        self.lineedit = rv_utl_widgets.RVSearch(icon_path=r":/resources/search_16.png", placeholder="输入镜头号")
        self.addWidget(self.lineedit)
        self.addSeparator()
        self.add_time_btn()
        #self.add_task_status_btn()
        self.addSeparator()
        self.add_refresh_btn()
        self.add_play_btn()
        self.lineedit.editingFinished.connect(self.filter_shot)
    
    def filter_shot(self):
        text = self.lineedit.text()
        self.table.filter_shot(text)

    def add_time_btn(self):
        time = QtWidgets.QToolButton()
        time.setIcon(QtGui.QPixmap(r":/resources/time_16.png"))
        self.time_menu = QtWidgets.QMenu(time)
        action_group = QtGui.QActionGroup(self.time_menu)
        action_group.setExclusionPolicy(QtGui.QActionGroup.ExclusionPolicy.ExclusiveOptional)
        action1 = self.time_menu.addAction("今天")
        action1.setCheckable(True)
        #action1.setChecked(True)
        action2 = self.time_menu.addAction("本周")
        action2.setCheckable(True)
        #action2.setChecked(True)
        action3 = self.time_menu.addAction("本月")
        action3.setCheckable(True)
        #action3.setChecked(True)
        action_group.addAction(action1)
        action_group.addAction(action2)
        action_group.addAction(action3)
        time.setAutoRaise(True)
        time.setMenu(self.time_menu)
        time.setPopupMode(QtWidgets.QToolButton.ToolButtonPopupMode.InstantPopup)
        time.setArrowType(QtCore.Qt.ArrowType.NoArrow)
        self.addWidget(time)
        self.time_menu.triggered.connect(self.__update_time_filter_data)
    
    def __update_time_filter_data(self, at: QtGui.QAction=None):
        result = []
        data = {"task_last_submit_time":result}
        today = datetime.today()
        end_time = today
        end_time = end_time
        for action in self.time_menu.actions():
            if not action.isChecked():
                continue
            time = action.text()
            start_time = ""
            if time == RVTableToolbar.TimeEnum.DAY.value:
                start_time = today - timedelta(days=-1)
            elif time == RVTableToolbar.TimeEnum.WEEK.value:
                weekday = today.weekday()
                if weekday == 0:
                    start_time = today.replace(hour=0, minute=0, second=0)
                else:
                    start_time = today - timedelta(days=weekday)
            elif time == RVTableToolbar.TimeEnum.MONTH.value:
                start_time = today - timedelta(days=today.day-1)
                start_time = start_time.replace(hour=0, minute=0, second=0)
            if start_time:
                result.append([start_time, end_time])
        self.table.set_filter_data(data)
    
    def add_task_status_btn(self):
        self.status = QtWidgets.QToolButton()
        self.status.setIcon(QtGui.QPixmap(r":/resources/status_16.png"))
        self.addWidget(self.status)
        self.status.setAutoRaise(True)
        self.status.setPopupMode(QtWidgets.QToolButton.ToolButtonPopupMode.InstantPopup)
        self.status.setArrowType(QtCore.Qt.ArrowType.NoArrow)
        self.status_dialog = RVStatusWidget(self)
        self.status.clicked.connect(self.show_status_list)
        self.status_dialog.item_clicked.connect(lambda x: self.status_changed.emit(x))
        self.status_dialog.on_item_clicked()


    def show_status_list(self):
        self.status_dialog.move(QtGui.QCursor.pos())
        self.status_dialog.show()
        ...
        #self.addWidget(status)
        
    
    def add_refresh_btn(self):
        refresh_btn = QtWidgets.QToolButton()
        refresh_btn.setIcon(QtGui.QPixmap(r":/resources/refresh_16.png"))
        self.addWidget(refresh_btn)
        refresh_btn.clicked.connect(self.table.reload)
    
    def add_play_btn(self):
        play_btn = QtWidgets.QToolButton()
        play_btn.setIcon(QtGui.QPixmap(r":/resources/play_32.png"))
        play_btn.clicked.connect(self.play)
        self.addWidget(play_btn)
        ...
    def play(self):
        self.table.play_selected()
        ...


class TableStatusBar(QtWidgets.QStatusBar):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setup()
        
    def setup(self):
        self.shot_label = QtWidgets.QLabel()
        self.shot_label.setText(f"镜头数量:")
        self.addWidget(self.shot_label)
    
    def update_shot(self, result):
        self.shot_label.setText(f"镜头数量: {result}")
        
class TableItem(QtWidgets.QWidget):
    
    def __init__(self, session, db_entity) -> None:
        super().__init__()
        self.left_icon = QtGui.QIcon(r":/resources/arrow_left.png")
        self.right_icon = QtGui.QIcon(r":/resources/arrow_right.png")
        self.setup(session, db_entity)
        
    
    def setup(self, session, db_entity):
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.setSpacing(0)
        layout1 = QtWidgets.QVBoxLayout()
        layout1.setContentsMargins(0,0,0,0)
        self.main_layout.setContentsMargins(0,0,0,0)
        self.status_bar = TableStatusBar()

        self.filter_widget = rv_filter_widget.FilterWidget()
        self.filter_widget.setContentsMargins(0,0,0,0)
        self.table = RVTable(session, db_entity, self.status_bar)
        toolbar = RVTableToolbar(self.table)
        toolbar.status_changed.connect(self.filter_widget.set_status_check_state)
        self.filter_widget.update_item_state.connect(self.table.set_filter_data)
        layout1.addWidget(toolbar)
        layout1.addWidget(self.table)
        layout1.addWidget(self.status_bar)
        self.main_layout.addLayout(layout1)
        self.side_btn = QtWidgets.QPushButton(self)
        self.side_btn.setObjectName("side_btn")
        self.side_btn.setFixedSize(10,35)
        self.side_btn.setIcon(self.left_icon)
        self.side_btn.setCheckable(True)
        self.side_btn.setChecked(False)
        self.side_btn.clicked.connect(self.__display_filter)
        self.table.resized.connect(self.__move_side_btn)
        self.main_layout.addWidget(self.filter_widget, 0, QtCore.Qt.AlignmentFlag.AlignRight)
        self.table.data_finished.connect(self.filter_widget.init_tree)
        self.table.setup()

    def __move_side_btn(self, size: QtCore.QSize):
        self.side_btn.move(size.width() - 15, size.height()/2)
        
    def __display_filter(self, state):
        if state:
            self.side_btn.setIcon(self.right_icon)
            self.filter_widget.setMinimumWidth(250)
        else:
            self.side_btn.setIcon(self.left_icon)
            self.filter_widget.setMaximumWidth(0)
            self.filter_widget.setMinimumWidth(0)

        
class RVTableContainer(QtWidgets.QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setup()
    
    def setup(self):
        self.stacked_layout = QtWidgets.QStackedLayout()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.addLayout(self.stacked_layout)

    
    def add_table(self, session, db_entity):
        self.stacked_layout.addWidget(TableItem(session, db_entity))
        
    def create_table(self, info):
        index = info.get("index")
        session = info.get("session")
        db_entity = info.get("db_entity")
        if index >= self.stacked_layout.count():
            self.add_table(session, db_entity)

    def switch_table(self, index):
        self.stacked_layout.setCurrentIndex(index)

    def close_table(self, index):
        if self.stacked_layout.count() == 1:
            return
        else:
            table = self.stacked_layout.widget(index)
            self.stacked_layout.removeWidget(table)
        

class RVTableVersionDialog(QtWidgets.QDialog):
    version_changed = QtCore.Signal(list)
    def __init__(self, data_dict, parent=None) -> None:
        super().__init__(parent)
        self.setup()
        self.setWindowTitle("选择版本")
        self.setWindowIcon(QtGui.QIcon(":/resources/version_16.png"))
        self.tree_init(data_dict)

    def setup(self):
        layout = QtWidgets.QVBoxLayout(self)
        self.tree_widget = QtWidgets.QTreeWidget()
        self.tree_widget.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.MultiSelection)
        self.ok_btn = QtWidgets.QPushButton()
        self.ok_btn.setText("Ok")
        layout.addWidget(self.tree_widget)
        layout.addWidget(self.ok_btn)
        self.ok_btn.clicked.connect(self.send_info)
    
    def send_info(self):
        item_list = self.tree_widget.selectedItems()
        result = []
        for item in item_list:
            result.append({"version_id": item.version_id, "entity":item.text(0), "task_id":item.task_id, "path":item.path})
        self.version_changed.emit(result)
        self.close()
        
    def tree_init(self, data_dict):
        for task_entity, version_list in data_dict.items():
            root = QtWidgets.QTreeWidgetItem(self.tree_widget)
            root.setText(0, task_entity)
            for version_info in version_list:
                version_item = QtWidgets.QTreeWidgetItem(root)
                version_item.task_id = version_info.get("#link_id")
                version_item.setText(0, version_info.get("entity"))
                version_item.version_id = version_info.get('#id')
                version_item.path = version_info.get('path')