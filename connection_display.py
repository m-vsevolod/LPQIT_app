from PyQt5.QtWidgets import QWidget, QPushButton
from readings import open_serial

class connection_display():

    def __init__(self, menu):
        super().__init__()
        self.menu = menu
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)

        self.connect_maestro_btn = QPushButton('Connect Maestro Powermeter')
        