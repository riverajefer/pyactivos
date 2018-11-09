#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from sys import platform
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QHBoxLayout,
QAction, qApp, QGroupBox, QDialog, QVBoxLayout, QGridLayout, QMainWindow)
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor
from PyQt5.QtCore import pyqtSlot, Qt
from sys import platform

class Menu(QMainWindow):
    def __init__(self, parent=None, DB=None):
        super(Menu, self).__init__(parent)
        self.DB = DB
        self.form_widget = FormWidget(self, DB) 
        self.setCentralWidget(self.form_widget) 
        self.menuTop()
        self.showFullScreen()
 
    def menuTop(self):
        exitAct = QAction(QIcon('salir.png'), '&SALIR', self)        
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Salir de la aplicación')
        exitAct.triggered.connect(qApp.quit)
        self.statusBar()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Archivo')
        fileMenu.addAction(exitAct)

 
class FormWidget(QWidget):

    def __init__(self, parent, DB=None):        
        super(FormWidget, self).__init__(parent)
        self.title = 'MENÚ'
        self.left = 500
        self.top = 350
        self.width = 800
        self.height = 400
        self.DB = DB
        self.initUI()
 

    def initUI(self):
        print('Menu paginas')
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.createGridLayout()
 
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)
 
        self.showFullScreen()

    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox("MENÚ PRINCIPAL")
         
        layout = QGridLayout()
        layout.setColumnStretch(1, 3)
 
        btnNuevo = QPushButton("NUEVO ACTIVO", self)
        btnNuevo.setFixedWidth(135)
        btnNuevo.setFixedHeight(80)
        
        btnNuevo.clicked.connect(self.gotToNuevoActivo)

        btnLectura = QPushButton(" LECTURA DE ACTIVO ", self)
        #btnLectura.setMinimumWidth(50)
        btnLectura.setFixedWidth(180)
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
    import sys
    app = QApplication([])
    foo = Menu()
    foo.showFullScreen()
    sys.exit(app.exec_())