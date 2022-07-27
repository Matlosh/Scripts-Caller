# Author: Matlosh, 2022
# https://github.com/Matlosh

import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QMainWindow, QLabel, QVBoxLayout, QMenuBar,
    QToolBar, QDockWidget, QSystemTrayIcon, QMenu, QHBoxLayout, QGridLayout
)
from PySide6.QtCore import Slot, Qt, QThread
from PySide6.QtGui import QIcon, QAction
from config import config
from components.application_topbar import ApplicationTopBar
from components.menu import Menu
from components.content import Content
from utils.functions import read_stylesheets, ExecuteScheduledCommands
from data.shared_data import SharedData

class ScriptsCaller(QMainWindow):

    def __init__(self):
        super().__init__()

        self.central_widget = QWidget()
        self.setWindowTitle('Scripts Caller')
        self.setWindowFlag(Qt.FramelessWindowHint, True)
        # self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowFlag(Qt.Tool, True)

        # Config settings
        self.resize(config['window_width'], config['window_height'])
        self.setFixedSize(config['window_width'], config['window_height'])

        self.shared_data = SharedData()

    def start(self):
        """Starts the application UI."""
        main_layout = QGridLayout()

        # Application Topbar (with exit, minimize button)
        application_topbar = ApplicationTopBar(parent_window=self)
        main_layout.addWidget(application_topbar, 0, 0)

        self.central_widget.setLayout(main_layout)
        self.setCentralWidget(self.central_widget)
        self.centralWidget().layout().setContentsMargins(0, 0, 0, 0)

        # Turns on scripts scheduler
        self.execute_scheduled_commands = ExecuteScheduledCommands()
        self.thread = QThread(self)
        self.execute_scheduled_commands.moveToThread(self.thread)

        self.thread.started.connect(
            self.execute_scheduled_commands.check_and_execute)

        # repair QThread error/warning here

        self.thread.finished.connect(
            self.execute_scheduled_commands.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(lambda: print('finished'))

        self.thread.start()

        # menu_n_content_layout = QGridLayout()
        # main_layout.addLayout(menu_n_content_layout)
        main_layout.setSpacing(0)

        # Application Content
        content = Content()
        main_layout.addWidget(content, 1, 1, 1, 3)

        # Application Menu
        menu = Menu(content, self.shared_data,
            self.execute_scheduled_commands)
        main_layout.addWidget(menu, 1, 0)

        # menu_n_content_layout.setColumnStretch(1, 1)
        # menu_n_content_layout.setSpacing(0)
        # menu_n_content_layout.setContentsMargins(0, 0, 0, 0)

        # Creates System Tray Icon (icon that's shown at the right side
        # of the bar - on Windows)
        tray_menu = QMenu('Scripts Caller', self)
        action = QAction('Option 1', tray_menu)
        action2 = QAction('Option 2', tray_menu)
        action3 = QAction('Option 3', tray_menu)
        tray_menu.addActions([action, action2, action3])

        tray_icon = QSystemTrayIcon(QIcon('assets/icons/app_icon.png'), self)
        tray_icon.setContextMenu(tray_menu)
        tray_icon.setToolTip('Scripts Caller')
        tray_icon.activated.connect(self.show_window)
        tray_icon.show()

        main_layout.setAlignment(Qt.AlignTop)
        read_stylesheets('styles/general.qss', self)
        self.show()

    def show_window(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.showNormal()

if __name__ == '__main__':
    app = QApplication([])
    # app.setQuitOnLastWindowClosed(False)
    scriptsCaller = ScriptsCaller()
    scriptsCaller.start()
    sys.exit(app.exec())