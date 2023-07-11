from PyQt5.QtWidgets import QWidget, QPushButton

class standa_spinner(QWidget):
    
    def __init__(self, menu):
        super().__init__()
        self.menu = menu
        self.title = 'Standa spinner | Лаборатория физики квантовых информационных технологий'
        self.initUI()

    def back_to_menu(self):
        self.close()
        self.menu.show()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.menu_btn = QPushButton('Home', self)
        self.menu_btn.clicked.connect(self.back_to_menu)

    