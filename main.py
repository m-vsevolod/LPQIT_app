from sys import argv, exit

from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QPushButton, QHBoxLayout, QWidget
from PyQt5.QtCore import Qt

from spd_counter import spd_counter

class MenuWindow(QMainWindow):
    def __init__(self):

        super().__init__()
        self.setWindowTitle('Лаборатория физики квантовых информационных технологий. Эксперимент')

        self.screen = QDesktopWidget().screenGeometry()
        self.width, self.height = 800, 600
        self.setGeometry(self.screen.width() // 2 - self.width // 2,
                          self.screen.height() // 2 - self.height // 2,
                          self.width, self.height)
        
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)

        self.spd_counter_btn = QPushButton('SPD counter')
        self.spd_counter_btn.clicked.connect(self.open_spd_counter)
        
        layout = QHBoxLayout()
        layout.addWidget(self.spd_counter_btn)

        central = QWidget()
        central.setLayout(layout)

        self.setCentralWidget(central)

    def open_spd_counter(self):
        self.close()
        self.spd_counter = spd_counter(self)
        self.spd_counter.show()

if __name__ == '__main__':
    app = QApplication(argv)
    main_window = MenuWindow()
    main_window.show()
    exit(app.exec_())
