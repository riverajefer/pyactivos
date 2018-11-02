#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget
from PyQt5.QtCore import QSize, QThread, pyqtSignal
import signal
from threading import Thread
import subprocess
try:
    import nfc
    import nfc.ndef
except ImportError:
    pass

class CloneThread(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self):
        QThread.__init__(self)
        self.git_url = ""
        self.clf = nfc.ContactlessFrontend('usb')

    # run method gets called when we start the thread
    def run(self):
        tag = self.clf.connect(rdwr={'on-connect': lambda tag: False})
        print(tag)
        self.signal.emit(tag)


class AsignarTagNFC(QMainWindow):
    def __init__(self, parent=None, idRow=None):
        super(AsignarTagNFC, self).__init__(parent)
        self.title = 'ASIGNAR TAG NFC'
        self.left = 500
        self.top = 350
        self.width = 800
        self.height = 400
        self.initUI()
        self.idRow = idRow
       

    def initUI(self):
         
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        self.setWindowTitle("ACERQUE SU TAG NFC AL LECTOR") 

        centralWidget = QWidget(self)          
        self.setCentralWidget(centralWidget)   

        gridLayout = QGridLayout(self)     
        centralWidget.setLayout(gridLayout)  

        title = QLabel("ACERQUE SU TAG NFC AL LECTOR", self) 
        title.setAlignment(QtCore.Qt.AlignCenter) 
        gridLayout.addWidget(title, 0, 0)
        self.show()

        self.git_thread = CloneThread()  # This is the thread object
        self.git_thread.start()
        self.git_thread.signal.connect(self.finished)
    
    def lecturaNFC(self):
        try:
            tag = self.clf.connect(rdwr={'on-connect': lambda tag: False})
            print(tag)
        except:
            pass

    def finished(self, result):
        print('result: ', result)


    
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AsignarTagNFC()
    sys.exit(app.exec_())