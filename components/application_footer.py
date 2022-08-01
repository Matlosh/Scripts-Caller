from PySide6.QtWidgets import QWidget, QLabel, QGridLayout
from PySide6.QtCore import Qt
from utils.functions import read_stylesheets

class ApplicationFooter(QWidget):
    
    def __init__(self):
        super().__init__()

        self.setObjectName('application_footer')
        self.setFixedSize(1000, 15)
        self.setAttribute(Qt.WA_StyledBackground)
        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        author = QLabel('Made by: Matlosh | 2022')
        author.setObjectName('application_footer_author')
        author.setAlignment(Qt.AlignLeft)
        version = QLabel('v0.0.0')
        version.setObjectName('application_footer_version')
        version.setAlignment(Qt.AlignRight)

        layout.addWidget(author, 0, 0, 1, 1)
        layout.addWidget(version, 0, 1, 1, 1)

        read_stylesheets('styles/application_footer.qss', self)