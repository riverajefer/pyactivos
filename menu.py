#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout, QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

class Menu(QDialog):
    def __init__(self, parent=None, DB=None):
        super(Menu, self).__init__(parent)
        self.title = 'MENÚ'
        self.left = 500
        self.top = 350
        self.width = 800
        self.height = 400
        self.DB = DB
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        self.createGridLayout()
 
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)
 
        self.show()
 
    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox("MENÚ PRINCIPAL")
         
        layout = QGridLayout()
        layout.setColumnStretch(1, 3)
 
        btnNuevo = QPushButton("NUEVO ACTIVO", self)
        btnNuevo.setFixedWidth(135)
        btnNuevo.setFixedHeight(80)
        
        btnNuevo.clicked.connect(self.gotToNuevoActivo)

        btnLectura = QPushButton("LECTURA DE ACTIVO", self)
        btnLectura.setFixedWidth(135)
        btnLectura.setFixedHeight(80)

        btnLectura.clicked.connect(self.gotToBuscarActivo)

        btnReporte = QPushButton("REPORTE", self)
        btnReporte.setFixedWidth(135)
        btnReporte.setFixedHeight(80)
        btnReporte.clicked.connect(self.gotToReportes)
        
        layout.addWidget(btnNuevo,0,0) 
        layout.addWidget(btnLectura,0,1) 
        layout.addWidget(btnReporte,0,2) 
 
        self.horizontalGroupBox.setLayout(layout)

    def gotToNuevoActivo(self):
        self.close()
        from paginas.NuevoActivo import NuevoActivo 
        self.SW = NuevoActivo(None, self.DB)

    def gotToBuscarActivo(self):
        self.close()
        from paginas.BuscarActivo import BuscarActivo 
        self.SW = BuscarActivo(None, self.DB)

    def gotToReportes(self):
        self.close()
        from paginas.Reportes import Reportes 
        self.SW = Reportes(None, self.DB)

 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Menu()
    sys.exit(app.exec_())