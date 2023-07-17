import sys
from PyQt5 import QtGui
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
        self.close_curtain_button = QPushButton("Close curtain")
        self.open_curtain_button = QPushButton("Open curtain")

        self.status_label = QLabel("Device is disconnected")
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
    
    def showEvent(self, event):
        """
        A function to update the list of the available COM-ports.
        """
        super().showEvent(event)
        self.com_port_combobox.clear()
        ports = serial.tools.list_ports.comports()
        for port, desc, hwid in ports:
            self.com_port_combobox.addItem("{}:{}".format(port, desc))

    def connect_device(self):
        """
        A function to connect the curtain. 
        """
        try:
            if self.serial and self.serial.is_open:
                self.status_label.setText("Curtain is already connected")
            else:
                selected_port = self.com_port_combobox.currentText().split(":")[0].strip()
                self.serial = serial.Serial(selected_port, baudrate=9600)
                self.status_label.setText("Curtain is connected")
                self.timer.start(1000)
        except serial.SerialException as e:
            self.status_label.setText("Curtain connection failed")

    def disconnect_device(self):
        """
        A function to disconnect from the curtain.
        """
        if self.serial:
            self.serial.close()
            self.serial = None
            self.status_label.setText("Curtain is disconnected")
        else:
            self.status_label.setText("Curtain disconnection failed")
        self.timer.stop()

    def update_status(self):
        """
        A function to get the status of the curtain.
        """
        try:
            if self.serial and self.serial.is_open:
                if self.serial.in_waiting:
                    data = self.serial.readline().decode().strip()
                    self.status_label.setText(f"Curtain connected - status: {data}")
                else:
                    self.status_label.setText("Curtain is connected")
            else:
                self.status_label.setText("Curtain is disconnected")
        except serial.SerialException as e:
            self.status_label.setText("Curtain connection Lost")
            self.disconnect_device()

    def close_curtain(self):
        """
        A function to close the curtain.
        """
        if self.serial and self.serial.is_open:
            turn_curtain(self.serial, 90)
            self.status_label.setText("Curtain is closed")
        else:
            self.status_label.setText("Curtain is not connected")

    def open_curtain(self):
        """
        A function to open the curtain.
        """
        if self.serial and self.serial.is_open:
            turn_curtain(self.serial, 0)
            self.status_label.setText("Curtain is opened")
        else:
            self.status_label.setText("Curtain is not connected")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = DeviceWidget()
    widget.show()
    sys.exit(app.exec_())