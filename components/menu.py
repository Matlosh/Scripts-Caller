from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QSizePolicy, QFrame
)
from PySide6.QtCore import Qt, QRect, QSize
from PySide6.QtGui import (
    QCursor, QMouseEvent, QIcon, QPixmap, QPaintEvent, QBrush, QColor,
    QPainter, QPalette, QImage, QPen
)
from utils.functions import read_stylesheets
from components.content import (
    ExecuteCommand, ScheduleCommand, ScheduledCommandsList, Settings
)

class Menu(QWidget):
    """Menu panel (on the left side of the app)"""
    
    def __init__(self, content_widget, shared_data, execute_scheduled_commands):
        super().__init__()
        self.setObjectName('menu_object')
        self.setFixedSize(300, 600)
        self.setAttribute(Qt.WA_StyledBackground)

        self.shared_data = shared_data
        self.content_widget = content_widget
        self.execute_scheduled_commands = execute_scheduled_commands
        self.layout = QVBoxLayout(self)

        insert_command = ExecuteCommand()
        menu_item_1 = MenuItem(text='Execute command', 
            icon='assets/icons/keyboard.svg',
            pressed_function=lambda: self.change_apps_content(insert_command))
        self.layout.addWidget(menu_item_1)

        schedule_command = ScheduleCommand(self.shared_data, 
            self.execute_scheduled_commands)
        menu_item_2 = MenuItem(text='Schedule command',
            icon='assets/icons/schedule.svg',
            pressed_function=lambda: self.change_apps_content(schedule_command))
        self.layout.addWidget(menu_item_2)

        scheduled_commands_list = ScheduledCommandsList(self.shared_data)
        menu_item_3 = MenuItem(text='Scheduled commands list',
            icon='assets/icons/list.svg',
            pressed_function=lambda: self.change_apps_content(
                scheduled_commands_list))
        self.layout.addWidget(menu_item_3)

        settings = Settings()
        menu_item_4 = MenuItem(text='Settings', 
            icon='assets/icons/settings.svg',
            pressed_function=lambda: self.change_apps_content(settings))
        self.layout.addWidget(menu_item_4)

        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)
        read_stylesheets('styles/menu.qss', self)

        # Setting default loaded content
        self.change_apps_content(schedule_command)

    def change_apps_content(self, content):
        if isinstance(content, ScheduledCommandsList):
            content.reload_list()
        self.content_widget.change_content(content)

    # now try to synchronize shared_data with other

    # @property
    # def shared_data(self):
    #     return self._shared_data

    # @shared_data.setter
    # def shared_data(self, new_shared_data):
    #     print('value changed')
    #     self._shared_data = new_shared_data

class MenuItem(QWidget):

    def __init__(self, text='', icon='', pressed_function=''):
        super().__init__()
        self.setObjectName('menu_item')
        self.text = text
        self.icon = icon
        self.pressed_function = pressed_function

        self.setFixedSize(300, 50)
        self.setCursor(Qt.PointingHandCursor)
        self.setAttribute(Qt.WA_StyledBackground)

    def mousePressEvent(self, event):
        if callable(self.pressed_function):
            self.pressed_function()
            return super().mousePressEvent(event)

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        
        painter.drawText(60, 31, self.text)
        painter.drawPixmap(10, 5, 40, 40, QIcon(self.icon).pixmap(40, 40))
        painter.end()