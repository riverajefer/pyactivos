#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from sys import platform
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QHBoxLayout, 
QGroupBox, QDialog, QVBoxLayout, 
QGridLayout, QMainWindow, QLabel, QLineEdit, QMessageBox)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, QThread, pyqtSignal
from threading import Thread
import signal
import subprocess
import time
import datetime
sys.path.append('..')

try:
    import nfc
except ImportError:
    pass

class NFCThread(QThread):
    signal = pyqtSignal('PyQt_PyObject')

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
 
        self.showFullScreen()
        #self.show()
 
    def buscarGridLayout(self):
        self.horizontalGroupBox = QGroupBox("BUSCAR ACTIVO")
         
        layout = QGridLayout()
      
        self.lblBuscar = QLabel('Número de activo')
        self.lblBuscar.setFixedWidth(100)
        self.lblBuscar.setFixedHeight(35)        

        self.inputBuscar = QLineEdit()
        self.inputBuscar.setFixedWidth(200)
        self.inputBuscar.setFixedHeight(35)
        self.inputBuscar.setText('123')
        
        self.btnBuscar = QPushButton("BUSCAR ACTIVO", self)
        self.btnBuscar.setFixedWidth(150)
        self.btnBuscar.setFixedHeight(35)
        self.btnBuscar.clicked.connect(self.buscarActivo)

        self.btnVolver = QPushButton("VOLVER", self)
        self.btnVolver.setFixedWidth(150)
        self.btnVolver.setFixedHeight(35)
        self.btnVolver.clicked.connect(self.volver)
        
        self.lblEtiqueta = QLabel('O ACERQUE LA ETIQUETA NFC')
        self.lblEtiqueta.setStyleSheet("QLabel {font-weight: bold;}")

        layout.addWidget(self.lblBuscar,0,0) 
        layout.addWidget(self.inputBuscar,0,1) 
        layout.addWidget(self.btnBuscar,0,2) 
        layout.addWidget(self.lblEtiqueta,1,1) 
        layout.addWidget(self.btnVolver,2,2) 
 
        self.horizontalGroupBox.setLayout(layout)

        if platform == "linux" or platform == "linux2":
            self.runNFC()

    
    def runNFC(self):
        self.nfc_thread = NFCThread()  # This is the thread object
        self.nfc_thread.start()
        self.nfc_thread.signal.connect(self.resultNFC)        
    
    
    def buscarActivo(self):
      numero = self.inputBuscar.text()
      id = self.DB.buscarPorNumero(str(numero))
      if id:
        self.goToDetalles(id)
        self.guardarRegistro(id)
      else:
        msg = QMessageBox()
        QMessageBox().setIcon(QMessageBox.Warning)
        msg.warning(self, "Error !", "Registro no encontrado")
        self.inputBuscar.setFocus()


    def resultNFC(self, tag):
      print('result: ', tag)
      id = self.DB.buscarPorTag(str(tag))
      if id:
        self.goToDetalles(id)
        self.guardarRegistro(id)
      else:
        msg = QMessageBox()
        QMessageBox().setIcon(QMessageBox.Warning)
        msg.warning(self, "Error !", "Registro no encontrado")
        self.inputBuscar.setFocus()
        self.runNFC()


    def volver(self):
      
      from menu import Menu
      self.SW = Menu(None, self.DB)
      self.close()

    def guardarRegistro(self, activo_id):
        columns = 'usuario_id, activo_id, fecha'
        usuario = 1
        fecha = datetime.datetime.now()
        data = " '"+str(usuario)+"', '"+str(activo_id)+"', '"+str(fecha)+"'"
        print(data)
        self.DB.write('usuario_activo', columns, data)     

    def goToDetalles(self, id):
        self.nfc_thread.stop()
        from paginas.DetallesActivo import DetallesActivo
        self.SW = DetallesActivo(None, self.DB, id)
        self.close()
 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BuscarActivo()
    sys.exit(app.exec_())