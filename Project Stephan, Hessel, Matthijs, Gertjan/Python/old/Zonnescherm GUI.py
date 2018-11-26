import sys
import time
from Connection import Main
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Main_Window(QWidget):

    serial = Main()
    grid = QGridLayout()
    connectedDevices = []
    connectedLabels = []
    unconnectedLabels = []
    
    def __init__(self):
        super().__init__()
        self.devices = {}
        
        LArd1 = QLabel("disconnected", self)
        Label_1 = QLabel("Arduino 1: ", self)
        LArd2 = QLabel("disconnected", self)
        Label_2 = QLabel("Arduino 2: ", self)
        LArd3 = QLabel("disconnected", self)
        Label_3 = QLabel("Arduino 3: ", self)
        LArd4 = QLabel("disconnected", self)
        Label_4 = QLabel("Arduino 4: ", self)
        LArd5 = QLabel("disconnected", self)
        Label_5 = QLabel("Arduino 5: ", self)

        self.grid.addWidget(Label_1, 2, 1)
        self.grid.addWidget(LArd1, 2, 2)
        self.grid.addWidget(Label_2, 3, 1)
        self.grid.addWidget(LArd2, 3, 2)
        self.grid.addWidget(Label_3, 4, 1)
        self.grid.addWidget(LArd3, 4, 2)
        self.grid.addWidget(Label_4, 5, 1)
        self.grid.addWidget(LArd4, 5, 2)
        self.grid.addWidget(Label_5, 6, 1)
        self.grid.addWidget(LArd5, 6, 2)

        self.unconnectedLabels.append(LArd1)
        self.unconnectedLabels.append(LArd2)
        self.unconnectedLabels.append(LArd3)
        self.unconnectedLabels.append(LArd4)
        self.unconnectedLabels.append(LArd5)
        
        self.serial.adddevice.connect(self.addDevice)
        self.serial.deldevice.connect(self.deleteDevice)

        self.initUI()
        self.serial.run()
    
    def initUI(self):
        # Label variables
        l1 = QLabel("Zonneschermen:", self)

        self.SArd1 = QSlider(Qt.Horizontal)
        self.SArd1.setMinimum(0)
        self.SArd1.setMaximum(100)
        self.SArd1.setValue(0)
        self.SArd1.setTickInterval(10)
        self.SArd1.setTickPosition(QSlider.TicksBelow)
        self.SArd2 = QSlider(Qt.Horizontal)
        self.SArd2.setMinimum(0)
        self.SArd2.setMaximum(100)
        self.SArd2.setValue(0)
        self.SArd2.setTickInterval(10)
        self.SArd2.setTickPosition(QSlider.TicksBelow)
        self.SArd3 = QSlider(Qt.Horizontal)
        self.SArd3.setMinimum(0)
        self.SArd3.setMaximum(100)
        self.SArd3.setValue(0)
        self.SArd3.setTickInterval(10)
        self.SArd3.setTickPosition(QSlider.TicksBelow)
        self.SArd4 = QSlider(Qt.Horizontal)
        self.SArd4.setMinimum(0)
        self.SArd4.setMaximum(100)
        self.SArd4.setValue(0)
        self.SArd4.setTickInterval(10)
        self.SArd4.setTickPosition(QSlider.TicksBelow)
        self.SArd5 = QSlider(Qt.Horizontal)
        self.SArd5.setMinimum(0)
        self.SArd5.setMaximum(100)
        self.SArd5.setValue(0)
        self.SArd5.setTickInterval(10)
        self.SArd5.setTickPosition(QSlider.TicksBelow)

        # Button Variables
        applyButton = QPushButton("Refresh")
        applyButton.clicked.connect(self.refresh)

        # QGridLayout

        self.grid.setSpacing(0)

        self.grid.addWidget(l1, -1, 0)

        self.grid.addWidget(self.SArd1, 2, 0)

        self.grid.addWidget(self.SArd2, 3, 0)

        self.grid.addWidget(self.SArd3, 4, 0)

        self.grid.addWidget(self.SArd4, 5, 0)

        self.grid.addWidget(self.SArd5, 6, 0)

        self.grid.addWidget(applyButton, 7, 0)

        self.setLayout(self.grid)

        self.resize(540, 450)
        self.center
        self.setWindowTitle('Zonnescherm UI')
        self.setWindowIcon(QIcon('Gui_Icon.png'))

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def addDevice(self, serialn, name, port):
        self.connectedDevices.append(serialn)
        i = 0
        index = len(self.connectedDevices)
        for device in self.connectedDevices:
            for label in self.unconnectedLabels:
                if i < 1:
                    doc = QTextDocument()
                    doc.setHtml(label.text())
                    qtext = doc.toPlainText()
                    if device == qtext:
                        print("success")
                    if device != qtext:
                        temp = str(serialn)
                        label.setText(temp)
                        print(label)
                        self.connectedLabels.append(label)
                        self.unconnectedLabels.remove(label)
                i += 1
                print(index)

    def deleteDevice(self, serialn):
        for label in self.connectedLabels:
            doc = QTextDocument()
            doc.setHtml(label.text())
            qtext = doc.toPlainText()
            if int(serialn) == int(qtext):
                i = 0
                while i < 6:
                    if label == self.connectedLabels[i]:
                        label.setText("Disconnected")
                        self.unconnectedLabels.insert(i, label)
                        self.connectedLabels.remove(label)
                        self.connectedDevices.remove(serialn)
                        i = 0
                        return
                    i += 1

    def refresh(self):
        self.serial.run()

if __name__ == '__main__':

    App = QApplication(sys.argv)
    M_Window = Main_Window()
    M_Window.show()
    sys.exit(App.exec())
