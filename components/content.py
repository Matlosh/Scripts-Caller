from PySide6.QtWidgets import QWidget, QGridLayout, QLabel, QDateTimeEdit
from PySide6.QtCore import Qt, QThread, Slot, QDateTime
from utils.functions import (
    ExecuteScheduledCommands, read_stylesheets, ExecuteCommandsOneAfterAnother,
    ExecuteCommandsAllAtOnce
)
from components.reusable import Button, InputBox, CheckBox, DateTimeInputBox
import subprocess
import shlex
import pathlib
import os
from multiprocessing import Process
from time import sleep
import signal
from functools import partial
import threading

class Content(QWidget):
    """App's content (center part of the app's GUI)"""
    
    def __init__(self):
        super().__init__()
        self.setObjectName('content')
        self.setAttribute(Qt.WA_StyledBackground)
        self.setFixedSize(700, 550)
        read_stylesheets('styles/content.qss', self)

        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.layout)

    def change_content(self, content):
        if self.layout.count() > 0:
            self.layout.itemAt(0).widget().setParent(None)
            
        self.current_content = content
        self.layout.addWidget(self.current_content)
        # self.layout.removeWidget(self.current_content)
        # self.current_content.deleteLater()
        # self.current_content = content
        # self.layout.addWidget(self.current_content)

class ExecuteCommand(QWidget):
    """
    Executes command (or commands if there is added more) in one of the two
    modes:
    - execute all commands at once
    - execute commands one after another
    """

    def __init__(self):
        super().__init__()
        self.setObjectName('insert_command')
        self.setAttribute(Qt.WA_StyledBackground)

        self.SCRIPT_DIR_PATH = pathlib.Path('..').parent \
            .absolute().__str__()
        # Contains list of all input boxes/commands to execute and their 
        # path boxes
        self.command_boxes = []
        self.execute_all_at_once = False

        self.layout = QGridLayout()
        self.layout.setAlignment(Qt.AlignCenter)

        # Start elements build
        self.execute_button = Button(width=200, height=50, text='Execute', 
            object_name='execute_button', 
            clicked_function=self.execute_button_clicked)
        self.add_box_button = Button(width=50, height=50, icon_width=50, 
            icon_height=50, icon_url='assets/icons/plus.svg',
            object_name='add_box_button', 
            clicked_function=self.add_command_row)
        self.execute_at_one_checkbox = CheckBox(width=200, height=50, 
            text='Execute all at once')

        self.layout.addWidget(self.execute_at_one_checkbox, 0, 0, 1, 1)
        self.layout.addWidget(self.execute_button, 0, 1, 1, 1)
        self.layout.addWidget(self.add_box_button, 0, 2, 1, 1)

        self.execute_at_one_checkbox.stateChanged.connect(self.change_execution_mode)

        self.add_command_row()

        self.setLayout(self.layout)

    def execute_button_clicked(self):
        command_boxes_values = []
        for command_box, path_box in self.command_boxes:
            command_boxes_values.append(
                [command_box.input_text, path_box.input_text])

        def execute_all_at_once():
            self.buttons = []

            def cancel_process(process, button_widget_pos):
                # Problems when process is another pyQt application - it
                # terminates app, but throws error/warning "Timers cannot
                # be stopped from another thread"
                process.terminate()
                process.send_signal(signal.CTRL_BREAK_EVENT)
                self.layout.removeWidget(self.buttons[button_widget_pos])
                self.buttons[button_widget_pos].deleteLater()
                self.buttons[button_widget_pos] = None

            @Slot(object, int)
            def initialize_button(process, process_pos):
                cancel_executing_button = Button(width=50, height=50, icon_width=50,
                    icon_height=50, icon_url='assets/icons/exit.svg',
                    object_name='cancel_executing_button',
                    clicked_function=partial(
                        lambda process, i: cancel_process(process, i),
                        process=process, i=process_pos))

                self.buttons.append(cancel_executing_button)
                self.layout.addWidget(cancel_executing_button, 
                    process_pos + 1, 2, 1, 1)

            @Slot(int)
            def remove_button(process_pos):
                if self.buttons[process_pos] is not None:
                    self.layout.removeWidget(self.buttons[process_pos])
                    self.buttons[process_pos].deleteLater()
                    self.buttons[process_pos] = None

            self.execute_button.setEnabled(False)

            self.execute_commands = ExecuteCommandsAllAtOnce(
                command_boxes_values)
            self.thread = QThread(self)
            self.execute_commands.moveToThread(self.thread)

            self.thread.started.connect(self.execute_commands.execute_commands)
            self.execute_commands.process_ready.connect(initialize_button)
            self.execute_commands.process_ended.connect(remove_button)

            self.execute_commands.finished.connect(self.thread.quit)
            self.thread.finished.connect(lambda: self.execute_button.setEnabled(True))
            self.thread.finished.connect(self.execute_commands.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)

            self.thread.start()

        def execute_one_after_another():
            cancel_process_button = Button(width=50, height=50, icon_width=50,
                icon_height=50, icon_url='assets/icons/exit.svg',
                object_name='cancel_executing_button')

            @Slot(int)      
            def create_button(pos):
                if pos > 1:
                    self.layout.removeWidget(cancel_process_button)
                self.layout.addWidget(cancel_process_button, pos, 2, 1, 1)

            def cancel_process(process):
                process.terminate()
                process.send_signal(signal.CTRL_BREAK_EVENT)

            self.execute_button.setEnabled(False)
            self.execute_commands = \
                ExecuteCommandsOneAfterAnother(command_boxes_values)
            self.thread = QThread(self)
            self.execute_commands.moveToThread(self.thread)

            self.thread.started.connect(
                self.execute_commands.execute_commands)
            self.execute_commands.command_num.connect(create_button)
            cancel_process_button.clicked.connect(
                lambda: cancel_process(self.execute_commands.current_process))

            self.execute_commands.finished.connect(self.thread.quit)
            self.thread.finished.connect(lambda: self.execute_button.setEnabled(True))
            self.thread.finished.connect(cancel_process_button.deleteLater)
            self.thread.finished.connect(self.execute_commands.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)

            self.thread.start()

        if self.execute_all_at_once:
            execute_all_at_once()
        else:
            execute_one_after_another()

    def add_command_row(self):
        command_box = InputBox(width=300, height=50,
            placeholder='Command to execute...', object_name='input_box')
        path_box = InputBox(width=200, height=50, value=self.SCRIPT_DIR_PATH,
            placeholder='Path to execute at...', object_name='input_box') 

        self.command_boxes.append([command_box, path_box])
        self.layout.addWidget(command_box, len(self.command_boxes), 0, 1, 1)
        self.layout.addWidget(path_box, len(self.command_boxes), 1, 1, 1)

    def change_execution_mode(self):
        self.execute_all_at_once = not self.execute_all_at_once

class ScheduleCommand(QWidget):

    def __init__(self, shared_data, execute_scheduled_commands):
        super().__init__()

        self.shared_data = shared_data
        self.execute_scheduled_commands = execute_scheduled_commands
        self.DEFAULT_SCRIPT_DIR_PATH = pathlib.Path('..').parent \
            .absolute().__str__()
        
        self.setObjectName('schedule_command')
        self.setAttribute(Qt.WA_StyledBackground)
        self.layout = QGridLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)

        self.schedule_boxes = []

        add_to_schedule_button = Button(width=200, height=50,
            text='Add to schedule',
            object_name='add_to_schedule_button',
            clicked_function=self.add_command_to_schedule)
        add_box_button = Button(width=50, height=50, icon_width=50,
            icon_height=50, icon_url='assets/icons/plus.svg',
            object_name='add_box_button',
            clicked_function=self.add_schedule_box)        

        # now add other compoenents to adding the new command to the schedule
        # trying to schedule and then save/load on program open/close

        self.layout.addWidget(add_to_schedule_button, 0, 1, 1, 1)
        self.layout.addWidget(add_box_button, 0, 2, 1, 1)

        self.add_schedule_box()

        self.setLayout(self.layout)

    def add_schedule_box(self):
        schedule_date_time = DateTimeInputBox(width=200, height=50)
        command_box = InputBox(width=300, height=50,
            placeholder='Command to schedule...', object_name='input_box')
        path_box = InputBox(width=200, height=50, value=self.DEFAULT_SCRIPT_DIR_PATH)

        self.schedule_boxes.append([schedule_date_time, command_box, path_box])
        schedule_boxes_len = len(self.schedule_boxes)

        self.layout.addWidget(schedule_date_time, 2 * schedule_boxes_len - 1, 
            0, 1, 1)
        self.layout.addWidget(command_box, 2 * schedule_boxes_len, 0, 1, 1)
        self.layout.addWidget(path_box, 2 * schedule_boxes_len, 1, 1, 1)

    def add_command_to_schedule(self):
        # below code is pretty ugly
        for schedule_date_time, command_box, path_box in self.schedule_boxes:
            schedule_box = [
                schedule_date_time.date_time,
                command_box.input_text,
                path_box.input_text    
            ]
            self.shared_data.scheduled_commands.append(schedule_box)
            self.execute_scheduled_commands.scheduled_commands \
                .append(schedule_box)
            self.layout.removeWidget(schedule_date_time)
            self.layout.removeWidget(command_box)
            self.layout.removeWidget(path_box)
            schedule_date_time.deleteLater()
            command_box.deleteLater()
            path_box.deleteLater()

        self.schedule_boxes.clear()
        self.add_schedule_box()

class ScheduledCommandsList(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QGridLayout(self)

        label = QLabel(self.__class__.__name__)
        self.layout.addWidget(label)

        self.setLayout(self.layout)

class Settings(QWidget):

    def __init__(self):
        super().__init__()

        self.setObjectName('settings')
        self.setAttribute(Qt.WA_StyledBackground)
        self.layout = QGridLayout(self)

        label = QLabel('Settings soon...')
        self.layout.addWidget(label, 0, 0, 1, 1)

        self.setLayout(self.layout)