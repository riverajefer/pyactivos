#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout, QMainWindow, QLabel, QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, QThread, pyqtSignal
from threading import Thread
import signal
import subprocess
import time
#from paginas.NuevoActivo import NuevoActivo 
#from paginas.AsignarTagNFC import AsignarTagNFC
sys.path.append('..')

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
        

    # run method gets called when we start the thread
    def run(self):
        after5s = lambda: time.time() - self.started > 15
        self.started = time.time()
        tag = self.clf.connect(rdwr={'on-connect': lambda tag: False}, terminate=after5s)
        try:
            self.tag_id = tag.identifier.encode('hex')
            print(self.tag_id)
            self.signal.emit(self.tag_id)
            self.clf.close()
        except Exception:
            print('terminado por tiempo')
            self.clf.close()

class BuscarActivo(QDialog):
    def __init__(self, parent=None, DB=None):
        super(BuscarActivo, self).__init__(parent)
        self.title = 'BUSCAR ACTIVO'
        self.left = 500
        self.top = 350
        self.width = 800
        self.height = 400
        self.DB = DB
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        self.buscarGridLayout()
 
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)
 
        self.show()
 
    def buscarGridLayout(self):
        self.horizontalGroupBox = QGroupBox("BUSCAR ACTIVO")
         
        layout = QGridLayout()
      
        self.lblBuscar = QLabel('Número de activo')
        self.lblBuscar.setFixedWidth(85)
        self.lblBuscar.setFixedHeight(35)        

        self.inputBuscar = QLineEdit()
        self.inputBuscar.setFixedWidth(200)
        self.inputBuscar.setFixedHeight(35)
        
        self.btnBuscar = QPushButton("BUSCAR ACTIVO", self)
        self.btnBuscar.setFixedWidth(150)
        self.btnBuscar.setFixedHeight(35)
        self.btnBuscar.clicked.connect(self.buscarActivo)


        self.btnVolver = QPushButton("VOLVER", self)
        self.btnVolver.setFixedWidth(150)
        self.btnVolver.setFixedHeight(35)
        self.btnVolver.clicked.connect(self.volver)
        
        self.lblEtiqueta = QLabel('O ACERQUE LA ETIQUETA NFC')

        
        layout.addWidget(self.lblBuscar,0,0) 
        layout.addWidget(self.inputBuscar,0,1) 
        layout.addWidget(self.btnBuscar,0,2) 
        layout.addWidget(self.lblEtiqueta,1,1) 
        layout.addWidget(self.btnVolver,2,2) 
 
        self.horizontalGroupBox.setLayout(layout)

        self.nfc_thread = NFCThread()  # This is the thread object
        self.nfc_thread.start()
        self.nfc_thread.signal.connect(self.finished)


    def buscarActivo(self):
      numero = self.inputBuscar.text()
      print('numero buscar: ', numero)
      if self.DB.buscarPorNumero(str(numero)):
        print('Ok encontrado')
        self.goToDetalles(1)
      else:
        print('No encontrado')


    def finished(self, tag):
      print('result: ', tag)

    def volver(self, tag):
      from menu import Menu
      self.SW = Menu(None, self.DB)
      self.close()

    def goToDetalles(self, id):
      from paginas.DetallesActivo import DetallesActivo
      self.SW = DetallesActivo(None, self.DB)
      self.close()


 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BuscarActivo()
    sys.exit(app.exec_())