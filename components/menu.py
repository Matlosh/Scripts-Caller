from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QSizePolicy, QFrame
)
from PySide6.QtCore import Qt, QRect, QSize
from PySide6.QtGui import (
    QCursor, QMouseEvent, QIcon, QPixmap, QPaintEvent, QBrush, QColor,
    QPainter, QPalette, QImage, QPen
)
from utils.functions import read_stylesheets
from components.content import ExecuteCommand, ScheduleCommand, Settings

class Menu(QWidget):
    """Menu panel (on the left side of the app)"""
    
    def __init__(self, content_widget):
        super().__init__()
        self.setObjectName('menu_object')
        self.setFixedSize(300, 600)
        self.setAttribute(Qt.WA_StyledBackground)
        self.content_widget = content_widget
        self.layout = QVBoxLayout(self)

        insert_command = ExecuteCommand()
        menu_item_1 = MenuItem(text='Execute command', 
            icon='assets/icons/keyboard.svg',
            pressed_function=lambda: self.change_apps_content(insert_command))
        self.layout.addWidget(menu_item_1)

        schedule_command = ScheduleCommand()
        menu_item_2 = MenuItem(text='Schedule command', 
            icon='assets/icons/schedule.svg',
            pressed_function=lambda: self.change_apps_content(schedule_command))
        self.layout.addWidget(menu_item_2)

        settings = Settings()
        menu_item_3 = MenuItem(text='Settings', 
            icon='assets/icons/settings.svg',
            pressed_function=lambda: self.change_apps_content(settings))
        self.layout.addWidget(menu_item_3)

        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)
        read_stylesheets('styles/menu.qss', self)

    def change_apps_content(self, content):
        self.content_widget.change_content(content)

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