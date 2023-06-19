from PyQt5.QtWidgets import QWidget, QPushButton

class spd_counter(QWidget):
    
    def __init__(self, menu):
        super().__init__()

        self.menu = menu

        self.title = 'SPD counter | Лаборатория физики квантовых информационных технологий'
        self.initUI()

    def initUI(self):

        self.setWindowTitle(self.title)

        self.test_button = QPushButton('test')

    