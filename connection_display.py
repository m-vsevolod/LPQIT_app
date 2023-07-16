import sys
import serial
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox
import serial.tools.list_ports

from readings import turn_curtain

class DeviceWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Curtain Widget")
        self.layout = QVBoxLayout()
        self.connect_button = QPushButton("Connect")
        self.disconnect_button = QPushButton("Disconnect")
        self.status_label = QLabel("Device is disconnected")
        self.close_curtain_button = QPushButton("Close curtain")
        self.open_curtain_button = QPushButton("Open curtain")

        self.com_port_combobox = QComboBox()

        self.layout.addWidget(self.com_port_combobox)
        self.layout.addWidget(self.connect_button)
        self.layout.addWidget(self.disconnect_button)
        self.layout.addWidget(self.open_curtain_button)
        self.layout.addWidget(self.close_curtain_button)
        self.layout.addWidget(self.status_label)
        self.setLayout(self.layout)

        self.connect_button.clicked.connect(self.connect_device)
        self.disconnect_button.clicked.connect(self.disconnect_device)
        self.open_curtain_button.clicked.connect(self.open_curtain)
        self.close_curtain_button.clicked.connect(self.close_curtain)

        self.serial = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status)

    def populate_com_ports(self):
        ports = serial.tools.list_ports.comports()
        self.com_port_combobox.addItem("hui")
        for port, desc, hwid in ports:
            self.com_port_combobox.addItem("hui")

    def connect_device(self):
        """
        A function to connect the device.
        """
        try:
            if self.serial and self.serial.is_open:
                self.status_label.setText("Device is already connected")
            else:
                selected_port = self.com_port_combobox.currentText().split(":")[0].strip()
                self.serial = serial.Serial(selected_port, baudrate=9600)
                self.status_label.setText("Device is connected")
                self.timer.start(1000)
        except serial.SerialException as e:
            self.status_label.setText("Device connection failed")

    def disconnect_device(self):
        if self.serial:
            self.serial.close()
            self.serial = None
            self.status_label.setText("Device is disconnected")
        else:
            self.status_label.setText("Device disconnection failed")
        self.timer.stop()

    def update_status(self):
        try:
            if self.serial and self.serial.is_open:
                if self.serial.in_waiting:
                    data = self.serial.readline().decode().strip()
                    self.status_label.setText(f"Device connected - status: {data}")
                else:
                    self.status_label.setText("Device is connected")
            else:
                self.status_label.setText("Device is disconnected")
        except serial.SerialException as e:
            self.status_label.setText("Device connection Lost")
            self.disconnect_device()

    def close_curtain(self):
        if self.serial and self.serial.is_open:
            turn_curtain(self.serial, 90)
            self.status_label.setText("Curtain is closed")
        else:
            self.status_label.setText("Device is not connected")

    def open_curtain(self):
        if self.serial and self.serial.is_open:
            turn_curtain(self.serial, 0)
            self.status_label.setText("Curtain is opened")
        else:
            self.status_label.setText("Device is not connected")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = DeviceWidget()
    widget.show()
    sys.exit(app.exec_())