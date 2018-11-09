#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
from sys import platform
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtCore import QSize, QThread, pyqtSignal
import signal
from threading import Thread
import subprocess
sys.path.append('..')
from DB.database import Database

try:
    import nfc
except ImportError:
    pass

class NFCThread(QThread):
    signal = pyqtSignal('PyQt_PyObject')
    __stop_reading = False

    def __init__(self):
        QThread.__init__(self)
        try:
            self.clf = nfc.ContactlessFrontend('usb')
        except Exception as err:
           print('Error NFC dispositivo')
        self.running = False

    def stop(self):
        self.running = False
        print('received stop signal from window.')
        self.clf.close()     

    def finNFC(self):
        return not self.running

    # run method gets called when we start the thread
    def _do_work(self):
        tag = self.clf.connect(rdwr={'on-connect': lambda tag: False}, terminate=self.finNFC)
        try:
            self.tag_id = tag.identifier.encode('hex')
            print(self.tag_id)
            self.signal.emit(self.tag_id)
            self.clf.close()
        except Exception:
            print('terminado por tiempo')
            self.clf.close()

    def run(self):
        self.running = True
        if self.running:
            self._do_work()  
        

class AsignarTagNFC(QMainWindow):
    def __init__(self, parent=None, idRow=8, DB=None):
        super(AsignarTagNFC, self).__init__(parent)
        self.title = 'ASIGNAR TAG NFC'
        self.left = 0
        self.top = 0
        self.width = 800
        self.height = 400
        self.initUI()
        self.idRow = idRow
        self.DB = DB
       
    def initUI(self):
         
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        self.setWindowTitle("ACERQUE SU TAG NFC AL LECTOR") 

        centralWidget = QWidget(self)          
        self.setCentralWidget(centralWidget)   

        gridLayout = QGridLayout(self)     
        centralWidget.setLayout(gridLayout)  

        self.title = QLabel("ACERQUE SU TAG NFC AL LECTOR", self) 
        self.title.setAlignment(QtCore.Qt.AlignCenter) 
        gridLayout.addWidget(self.title, 0, 0)

        self.button = QPushButton('CANCELAR', self)
        self.button.clicked.connect(self.volver)
        self.button.setFixedWidth(135)
        self.button.setFixedHeight(80)
        gridLayout.addWidget(self.button, 1, 0)
        
        #self.show()
        self.showFullScreen()

        if platform == "linux" or platform == "linux2":
            self.runNFC()

    def runNFC(self):
        self.nfc_thread = NFCThread()  # This is the thread object
        self.nfc_thread.start()
        self.nfc_thread.signal.connect(self.resultNFC)     
    
    def resultNFC(self, tag):
        print('result: ', tag)
        if not self.DB.existeNFC(str(tag)):

            if self.DB.addTagToId(str(tag), self.idRow):
                print("ASIGANADO CORRECTAMENTE")
                self.title.setText("ASIGANADO CORRECTAMENTE") 
                self.button.setText('VOLVER AL MENÚ')
            else:
                print("ERROR")
        else:
            print('Error')
            self.title.setText("ERROR, ESTÁ ETIQUETA YA HA SIDO ASIGNADA A UN ACTIVO, ACERQUE OTRA ") 
            self.runNFC()


    def volver(self):
        self.nfc_thread.stop()
        self.close()
        from menu import Menu
        self.SW = Menu(None, self.DB)
    
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AsignarTagNFC()
    sys.exit(app.exec_())