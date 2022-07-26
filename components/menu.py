from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QSizePolicy, QFrame
)
from PySide6.QtCore import Qt, QRect, QSize
from PySide6.QtGui import (
    QCursor, QMouseEvent, QIcon, QPixmap, QPaintEvent, QBrush, QColor,
    QPainter, QPalette, QImage, QPen
)
from utils.functions import read_stylesheets

class Menu(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setObjectName('menu_object')
        self.setFixedSize(300, 600)
        self.setAttribute(Qt.WA_StyledBackground)
        self.layout = QVBoxLayout(self)

        menu_item_1 = MenuItem(text='Item 1', icon='assets/icons/exit.svg',
            pressed_function=self.button_press_1)
        self.layout.addWidget(menu_item_1)
        menu_item_2 = MenuItem(text='Item 2', icon='assets/icons/app_icon.png',
            pressed_function=self.button_press_1)
        self.layout.addWidget(menu_item_2)
        menu_item_3 = MenuItem(text='Item 2', icon='assets/icons/app_icon.png',
            pressed_function=self.button_press_1)
        self.layout.addWidget(menu_item_3)

        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)
        read_stylesheets('styles/menu.qss', self)

    def button_press_1(self):
        print('button pressed')

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
        
        painter.drawText(50, 31, self.text)
        painter.drawPixmap(5, 5, 40, 40, QIcon(self.icon).pixmap(40, 40))
        painter.end()