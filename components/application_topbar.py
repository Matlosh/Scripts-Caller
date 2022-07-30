from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, QPushButton,
    QApplication, QFrame
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QCursor, QMouseEvent
from utils.functions import read_stylesheets
from components.reusable import Button
from data.shared_data import SharedData

class ApplicationTopBar(QWidget):
    """Widget which contains exit and minimize button."""

    def __init__(self, parent_window: QWidget, shared_data: SharedData):
        super().__init__()
        self.parent_window = parent_window
        self.drag_mouse_pos = ''
        self.shared_data = shared_data
        self.setObjectName('application_topbar')
        self.setAttribute(Qt.WA_StyledBackground)
        self.startUI()

    def startUI(self):
        self.layout = QHBoxLayout()

        # Minimize button
        self.minimize_button = Button(width=50, height=50, icon_width=30, icon_height=30,
            icon_url='assets/icons/minimize.svg',
            clicked_function=self.minimize_application, object_name='minimize_button')
        self.layout.addWidget(self.minimize_button)

        # Exit button
        self.exit_button = Button(width=50, height=50, icon_width=30, icon_height=30, 
            icon_url='assets/icons/exit.svg', 
            clicked_function=self.close_application, object_name='exit_button')
        self.layout.addWidget(self.exit_button)

        # Setting layout
        self.layout.setAlignment(Qt.AlignRight)
        self.setLayout(self.layout)
        self.setFixedSize(1000, 50)
        self.layout.setContentsMargins(0, 0, 0, 0)

        read_stylesheets('styles/application_topbar.qss', self)
        # now repair app's movement error when move=nig after clicking on topbar's button

    def close_application(self):
        self.shared_data.save_to_file()
        QApplication.exit()

    def minimize_application(self):
        self.parent_window.showMinimized()

    def mousePressEvent(self, event: QMouseEvent):
        self.drag_mouse_pos = event.position()
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() and not self.minimize_button.underMouse() \
            and not self.exit_button.underMouse():
            mouse_pos = event.globalPosition().toPoint()
            self.parent_window.move(
                mouse_pos.x() - self.drag_mouse_pos.x(),
                mouse_pos.y() - self.drag_mouse_pos.y()
            )
            
        return super().mouseMoveEvent(event)