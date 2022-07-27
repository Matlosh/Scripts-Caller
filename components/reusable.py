from PySide6.QtWidgets import (
    QWidget, QAbstractButton, QVBoxLayout, QPushButton, QLabel,
    QLineEdit, QCheckBox, QDateTimeEdit
)
from PySide6.QtCore import Qt, QSize, QRect, QDateTime
from PySide6.QtGui import QIcon, QCursor, QPainter, QMouseEvent
from utils import functions

class Button(QPushButton):
    
    def __init__(self, *, width, height, text='', icon_width=0, icon_height=0,
        icon_url='', hover_cursor=Qt.PointingHandCursor, clicked_function='', 
        object_name='button', parent=None):
        super().__init__()

        if parent is not None:
            self.setParent(parent)

        self.setObjectName(object_name)
        self.setMaximumSize(width, height)
        self.setText(text)
        self.setIcon(QIcon(icon_url))
        self.setIconSize(QSize(icon_width, icon_height))
        self.setCursor(QCursor(hover_cursor))
        functions.read_stylesheets('styles/reusable.qss', self)

        if callable(clicked_function):
            self.clicked.connect(clicked_function)

class Label(QLabel):

    def __init__(self, *, width, height, text='', object_name='label'):
        super().__init__()
        
        self.setObjectName(object_name)
        self.setFixedSize(width, height)
        self.setText(text)
        functions.read_stylesheets('styles/reusable.qss', self)

class InputBox(QLineEdit):
    
    def __init__(self, *, width, height, value='', placeholder='',
        object_name='input_box'):
        super().__init__()

        self.object_name = object_name
        self.input_text = value

        self.setObjectName(self.object_name)
        self.setFixedSize(width, height)
        self.setText(value)
        self.setPlaceholderText(placeholder)
        functions.read_stylesheets('styles/reusable.qss', self)

        self.textChanged.connect(self.changePlaceholder)

    def changePlaceholder(self, text: str):
        self.input_text = text
        if len(text) > 0:
            if not self.object_name.endswith('_not_empty'):
                self.object_name += '_not_empty'
        elif (index := self.object_name.rfind('_not_empty')) != 0:
                self.object_name = self.object_name[0:index]
        # here add changing of input's text colour

class CheckBox(QCheckBox):

    def __init__(self, *, width, height, text='', object_name='check_box'):
        super().__init__()

        self.setObjectName(object_name)
        self.setFixedSize(width, height)
        self.setText(text)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        functions.read_stylesheets('styles/reusable.qss', self)

class DateTimeInputBox(QDateTimeEdit):
    
    def __init__(self, *, width, height, object_name='date_time_input_box', 
        start_date=QDateTime.currentDateTime(), show_calendar_popup=True,
        display_format='dd/MM/yyyy HH:mm:ss'):
        super().__init__()

        self.date_time = start_date

        self.setObjectName(object_name)
        self.setFixedSize(width, height)
        self.setDateTime(start_date)
        self.setCalendarPopup(show_calendar_popup)
        self.setDisplayFormat(display_format)
        functions.read_stylesheets('styles/reusable.qss', self)
        self.dateTimeChanged.connect(self.date_time_changed)

    def date_time_changed(self, date_time):
        self.date_time = date_time