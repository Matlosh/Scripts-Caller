from sys import stdout
from PySide6.QtCore import QObject, Signal, Slot
import subprocess, shlex
from time import sleep
import signal
import subprocess
from components.reusable import Button
from functools import partial
import time

def read_stylesheets(path_to_stylesheet, qwidget):
    """Reads stylesheet and sets in on the passed widget."""

    style_variables = {}

    # Gets all variables from the "variables.qss" file
    with open('styles/variables.qss') as variables:
        for line in variables:
            line = line.replace(' ', '')

            if line[0] == '@':
                colon_index = line.index(':')
                key = line[0:colon_index]
                value = line[colon_index+1:-2]
                style_variables[key] = value

    # Formats qss replace variables with values
    with open(path_to_stylesheet, 'r') as styles_general:
        stylesheet = ''

        for line in styles_general:
            # removing whitespaces isn't bad, but doesn't allow to use
            # styles with spaces between values (f.e. border: 1px solid red)
            # line = line.replace(' ', '')

            if '@' in line:
                key = line[line.index('@'):-2]
                if key in style_variables:
                    line = line.replace(key, style_variables[key])

            stylesheet += line

    qwidget.setStyleSheet(stylesheet)
    return stylesheet

class ExecuteCommandsOneAfterAnother(QObject):
    """
    Executes given command boxes one after another.
    
    Contains signals:
    - command_num - signal emitted every change of executed command, returns
        position of the currently executed command box in given command boxes 
        list
    - finished - signal emitted when all commands are executed"""
    command_num = Signal(int)
    finished = Signal()

    def __init__(self, command_boxes_values):
        super().__init__()
        self.command_boxes_values = command_boxes_values
        self.current_process = None

    def execute_commands(self):
        for i, (command_box_value, path_box_value) in \
            enumerate(self.command_boxes_values):

            self.command_num.emit(i + 1)
            self.current_process = subprocess.Popen(command_box_value,
                stdout=subprocess.PIPE, shell=True,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
                cwd=path_box_value)

            self.current_process.wait()

        self.finished.emit()

class ExecuteCommandsAllAtOnce(QObject):
    """
    Executes all given commands at once.
    
    Contains signals:
    - process_ready - signal emitted when process was fired and is ready 
        "to work", returns fired process and it's position in the given 
        command boxes list
    - process_ended - signal emitted when one of the given processes has 
        ended, returns position of that process
    - finished - signal emitted when all of the processes have ended
    """
    process_ready = Signal(object, int)
    process_ended = Signal(int)
    finished = Signal()

    def __init__(self, command_boxes_values):
        super().__init__()
        self.command_boxes_values = command_boxes_values
        self.processes = []

    def execute_commands(self):
        for i, (command_box_value, path_box_value) in \
            enumerate(self.command_boxes_values):

            process = subprocess.Popen(command_box_value,
                stdout=subprocess.PIPE, shell=True,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
                cwd=path_box_value)

            sleep(0.1)
            self.processes.append(process)

            self.process_ready.emit(process, i)

        while any(self.processes):
            for i, process in enumerate(self.processes):
                if process is not None:
                    process.poll()
                    if process.returncode is not None:
                        self.process_ended.emit(i)
                        self.processes[i] = None
            sleep(0.1)

        self.finished.emit()

class ExecuteScheduledCommands(QObject):
    """
    Checks if any of the expected execute time for command has passed and -
        if yes - executes that command.
    Note: It is recommended to create an object of this class only once and
        just update its scheduled commands list in order to prevent from
        executing the same scheduled commands few times

    scheduled_commands pattern:
        - at index 0 - planned date and time to execute command (as QDateTime)
        - at index 1 - command to execute (as str)
        - at index 2 - path to execute command at (as str)
    """

    def __init__(self, scheduled_commands=[]):
        super().__init__()
        self.scheduled_commands = scheduled_commands

    def check_and_execute(self):
        while True:
            for scheduled_command in self.scheduled_commands:
                current_time = int(time.time())
                if current_time == scheduled_command[0].toSecsSinceEpoch():
                    process = subprocess.Popen(scheduled_command[1],
                        stdout=subprocess.PIPE, shell=True,
                        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
                        cwd=scheduled_command[2])
            sleep(1)