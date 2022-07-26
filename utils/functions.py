from sys import stdout
from PySide6.QtCore import QObject, Signal, Slot
import subprocess, shlex
from time import sleep
import signal
import subprocess
from components.reusable import Button
from functools import partial

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

# class ExecuteCommands:

#     def execute_command_from_text(text, execute_path, stdin=None):
#         """Executes command given from text and returns cmd's output."""
#         output = ''
#         commands = shlex.split(text)
#         print(commands)
#         print(execute_path)
#         # commands = text

#         if stdin is not None:
#             output = subprocess.Popen(commands, stdin=stdin.stdout, 
#                 stdout=subprocess.PIPE, shell=True, cwd=execute_path)
#         else:
#             output = subprocess.Popen(commands, stdout=subprocess.PIPE, 
#                 shell=True, cwd=execute_path)

#         return output
    
#     def execute_all_commands(*command_boxes):
#         # finished = Signal()
#         # progress = Signal(int)

#         last_output = None
#         for i, (command_box_value, path_box_value) in \
#             enumerate(command_boxes):

#             if last_output is not None:
#                 # Below line is commented, because of I/O error
#                 # All scripts/commands are executed just in order, their
#                 # inputs aren't related or anything
#                 # last_output = self.execute_command_from_text(
#                 #     command_box.input_text, path_box.input_text,
#                 #     last_output)
#                 last_output = ExecuteCommands.execute_command_from_text(
#                     command_box_value, path_box_value
#                 )
#             else:
#                 last_output = ExecuteCommands.execute_command_from_text(
#                     command_box_value, path_box_value)

#             print(last_output.communicate()[0].decode())
#         #     progress.emit(i + 1)

#         # finished.emit()

class ExecuteCommandsOneAfterAnother(QObject):
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
    process_ready = Signal(object, int)
    loaded = Signal()
    process_ended = Signal(int)

    def __init__(self, command_boxes_values, parent):
        super().__init__()
        self.parent = parent
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

        self.loaded.emit()

        while any(self.processes):
            for i, process in enumerate(self.processes):
                if process is not None:
                    process.poll()
                    if process.returncode is not None:
                        self.process_ended.emit(i)
                        self.processes[i] = None
            sleep(0.1)