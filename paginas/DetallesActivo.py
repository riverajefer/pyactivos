#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from os import getcwd, path
import os
import shutil
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QHBoxLayout, 
QGroupBox, QDialog, QVBoxLayout, QGridLayout, 
QMainWindow, QLabel, QLineEdit, QTextEdit,
QComboBox, QCalendarWidget, QFileDialog, QMessageBox, QDateEdit, QCheckBox)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot, QDate, Qt, pyqtSignal, QByteArray, QIODevice, QBuffer, QDateTime
from pathlib import Path
sys.path.append('..')
from paginas.AsignarTagNFC import AsignarTagNFC


class QLabelClickable(QLabel):
    clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super(QLabelClickable, self).__init__(parent)

    def mousePressEvent(self, event):
        self.clicked.emit()    

class DetallesActivo(QDialog):
    def __init__(self, parent=None, DB=None, ID=None):
        super(DetallesActivo, self).__init__(parent)
        self.title = 'DETALLES ACTIVO'
        self.left = 500
        self.top = 350
        self.width = 800
        self.height = 400        
        self.DB = DB
        self.id = ID
        self.detalles='';
        self.fechaIngreso = '';
        self.initUI()
        
    def initUI(self):
        self.detalles = self.DB.getPorId(self.id);

        print("DETALLES: ", self.detalles)
        print('Detalles numero: ', self.detalles[0][1])
        
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.widthtInput = 350
        self.heightInput = 25

        lblNumeroActivo = QLabel('Número de Activo')
        lblNumeroActivo.setStyleSheet("QLabel {font-weight: bold;}")

        lblResponsable = QLabel('Responsable')
        lblResponsable.setStyleSheet("QLabel {font-weight: bold;}")

        lblDepartamento = QLabel('Departamento')
        lblDepartamento.setStyleSheet("QLabel {font-weight: bold;}")

        lblFechaIngreso = QLabel('Fecha de Ingreso')
        lblFechaIngreso.setStyleSheet("QLabel {font-weight: bold;}")

        lblDescripcion = QLabel('Descripcion')
        lblDescripcion.setStyleSheet("QLabel {font-weight: bold;}")

        self.checkObsoleto = QCheckBox("ACTIVO OBSOLETO")
        self.checkObsoleto.stateChanged.connect(lambda:self.cambioCheck(self.checkObsoleto))

        self.departamento = QLineEdit()
        self.departamento.setFixedWidth(self.widthtInput)
        self.departamento.setText(self.detalles[0][3])
        self.departamento.setDisabled(True)        

        self.editNumeroActivo = QLineEdit()
        self.editNumeroActivo.setFixedWidth(self.widthtInput)
        self.editNumeroActivo.setFixedHeight(self.heightInput)

        self.editNumeroActivo.setDisabled(True)
        self.editNumeroActivo.setText(self.detalles[0][1])

        self.editResponsable = QLineEdit()
        self.editResponsable.setFixedWidth(self.widthtInput)
        self.editResponsable.setFixedHeight(self.heightInput)

        self.editResponsable.setDisabled(True)
        self.editResponsable.setText(self.detalles[0][4])

        self.editDescripcion = QTextEdit()
        self.editDescripcion.setFixedWidth(self.widthtInput)
        self.editDescripcion.setDisabled(True)
        self.editDescripcion.setText(self.detalles[0][2])

        self.fecha = QLineEdit()
        self.fecha.setFixedWidth(self.widthtInput)
        self.fecha.setText(self.detalles[0][5])
        self.fecha.setDisabled(True)

        self.labelImagen = QLabel(self)
        self.labelImagen.setFixedWidth(180)
        self.labelImagen.setFixedHeight(180)

        self.labelImagen.setStyleSheet("QLabel {background-color: white; border: 1px solid "
                                       "#01DFD7; border-radius: 2px;}")
        
        self.labelImagen.setAlignment(Qt.AlignCenter)
        ruta = 'imgs/activos/'+self.detalles[0][8]
        print('ruta: ', ruta)

        pixmapImagen = QPixmap(ruta).scaled(180, 180, Qt.KeepAspectRatio,
                                                  Qt.SmoothTransformation)

        # Mostrar imagen
        self.labelImagen.setPixmap(pixmapImagen)
        self.btnGuardar = QPushButton("GUARDAR", self)
        self.btnGuardar.setFixedWidth(180)
        self.btnGuardar.setFixedHeight(35)        
        self.btnGuardar.clicked.connect(self.guardar)
        self.btnGuardar.setDisabled(True)

        self.btnVolver = QPushButton("VOLVER", self)
        self.btnVolver.setFixedWidth(180)
        self.btnVolver.setFixedHeight(35)        
        self.btnVolver.clicked.connect(self.volver)

        grid = QGridLayout()
        grid.setSpacing(15)

        grid.addWidget(lblNumeroActivo, 0, 0)
        grid.addWidget(self.editNumeroActivo, 1, 0)

        grid.addWidget(lblResponsable, 2, 0)
        grid.addWidget(self.editResponsable, 3, 0)

        grid.addWidget(lblDepartamento, 4, 0)
        grid.addWidget(self.departamento, 5, 0)

        grid.addWidget(lblFechaIngreso, 6, 0)
        grid.addWidget(self.fecha, 7, 0)

        grid.addWidget(lblDescripcion, 8, 0)
        grid.addWidget(self.editDescripcion, 9, 0, 1, 0)

        grid.addWidget(self.labelImagen, 1, 1, 6, 5)
        grid.addWidget(self.btnVolver, 4, 5)

        if self.DB.userIsAdmin():
            grid.addWidget(self.checkObsoleto, 7, 1)
            grid.addWidget(self.btnGuardar, 3, 5)
        else:
            self.checkObsoleto.hide()
            self.btnGuardar.hide()

        self.setLayout(grid) 
        #self.show()
        self.showFullScreen()

    def cambioCheck(self,b):
        self.btnGuardar.setDisabled(not b.isChecked())

    def showDate(self, date):
        print(date.toString())        
        self.fechaIngreso = date.toString();
 
    def guardar(self):
        print('Guardar...')
        self.DB.toggleObsoleto(1, self.id)
        msg = QMessageBox()
        msg.information(self, "Ok !", "Guardado Correctamente")        
        print('Ok')


    def volver(self, tag):
      from menu import Menu
      self.SW = Menu(None, self.DB)
      self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DetallesActivo()
    sys.exit(app.exec_())

