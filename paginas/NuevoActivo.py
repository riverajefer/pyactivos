#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from os import getcwd, path
import os
import shutil
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QHBoxLayout, 
QGroupBox, QDialog, QVBoxLayout, QGridLayout, 
QMainWindow, QLabel, QLineEdit, QTextEdit,
QComboBox, QCalendarWidget, QFileDialog, QMessageBox, QDateEdit)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot, QDate, Qt, pyqtSignal, QByteArray, QIODevice, QBuffer, QDateTime
from pathlib import Path
sys.path.append('..')
from paginas.AsignarTagNFC import AsignarTagNFC

from DB.database import Database

db_path = 'db.db'
DB = Database()
DB.open(db_path)
reload(sys)  
sys.setdefaultencoding('utf8')

class QLabelClickable(QLabel):
    clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super(QLabelClickable, self).__init__(parent)

    def mousePressEvent(self, event):
        self.clicked.emit()    

class NuevoActivo(QDialog):
    def __init__(self, parent=None, DB=None):
        super(NuevoActivo, self).__init__(parent)
        self.title = 'MENÚ'
        self.left = 500
        self.top = 350
        self.width = 800
        self.height = 400        
        self.initUI()
        self.DB = DB
        self.fechaIngreso = '';
        
    def initUI(self):
        
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.widthtInput = 350
        self.heightInput = 25

        lblNumeroActivo = QLabel('Número de Activo')
        lblResponsable = QLabel('Responsable')
        lblDepartamento = QLabel('Departamento')
        lblFechaIngreso = QLabel('Fecha de Ingreso')
        lblDescripcion = QLabel('Descripcion')

        self.comboDepartamento = QComboBox(self)
        self.comboDepartamento.addItems(["Contabilidad", "Tecnología"])
        self.comboDepartamento.setCurrentIndex(0)
        self.comboDepartamento.setFixedWidth(self.widthtInput)
        self.comboDepartamento.setFixedHeight(self.heightInput)

        self.editNumeroActivo = QLineEdit()
        self.editNumeroActivo.setFixedWidth(self.widthtInput)
        self.editNumeroActivo.setFixedHeight(self.heightInput)

        self.editResponsable = QLineEdit()
        self.editResponsable.setFixedWidth(self.widthtInput)
        self.editResponsable.setFixedHeight(self.heightInput)

        self.editDescripcion = QTextEdit()
        self.editDescripcion.setFixedWidth(self.widthtInput)

        self.fecha = QDateEdit(self)
        self.fecha.setDateTime(QDateTime.currentDateTime())
        self.fecha.setCalendarPopup(True)

        self.labelImagen = QLabelClickable(self)
        self.labelImagen.setFixedWidth(180)
        self.labelImagen.setFixedHeight(180)
        self.labelImagen.setToolTip("Imagen")
        self.labelImagen.setCursor(Qt.PointingHandCursor)

        self.labelImagen.setStyleSheet("QLabel {background-color: white; border: 1px solid "
                                       "#01DFD7; border-radius: 2px;}")
        
        self.labelImagen.setAlignment(Qt.AlignCenter)

        self.btnSeleccionar = QPushButton("Seleccionar Imagen", self)
        self.btnSeleccionar.setToolTip("Seleccionar imagen")
        self.btnSeleccionar.setFixedWidth(180)
        self.btnSeleccionar.setFixedHeight(25)        
        self.btnSeleccionar.setCursor(Qt.PointingHandCursor)

        # Llamar función al hacer clic sobre el label
        self.labelImagen.clicked.connect(self.seleccionarImagen)
        self.btnSeleccionar.clicked.connect(self.seleccionarImagen)
     
        self.btnGuardar = QPushButton("GUARDAR", self)
        self.btnGuardar.setFixedWidth(180)
        self.btnGuardar.setFixedHeight(35)        
        self.btnGuardar.clicked.connect(self.guardar)

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
        grid.addWidget(self.comboDepartamento, 5, 0)

        grid.addWidget(lblFechaIngreso, 6, 0)
        grid.addWidget(self.fecha, 7, 0)

        grid.addWidget(lblDescripcion, 8, 0)
        grid.addWidget(self.editDescripcion, 9, 0, 1, 0)

        grid.addWidget(self.btnSeleccionar, 0, 1)
        grid.addWidget(self.labelImagen, 1, 1, 5, 5)
        grid.addWidget(self.btnGuardar, 3, 5)
        grid.addWidget(self.btnVolver, 4, 5)

        self.setLayout(grid) 
        #self.show()
        self.showFullScreen()

    def showDate(self, date):
        print(date.toString())        
        self.fechaIngreso = date.toString();
 
    def seleccionarImagen(self):
        self.rutaImagen, extension = QFileDialog.getOpenFileName(self, "Seleccionar imagen", getcwd(),
                                                        "Archivos de imagen (*.png *.jpg)",
                                                        options=QFileDialog.Options())
        
        self.nombreImagen = path.basename(self.rutaImagen)

        if self.rutaImagen:
            pixmapImagen = QPixmap(self.rutaImagen).scaled(180, 180, Qt.KeepAspectRatio,
                                                  Qt.SmoothTransformation)

            self.labelImagen.setPixmap(pixmapImagen)
    
    def guardar(self):
        temp_var  = self.fecha.date()
        fechaIngreso = temp_var.toPyDate()
        responsble = self.editResponsable.text()
        descripcion = self.editDescripcion.toPlainText()
        departamento = self.comboDepartamento.currentText()
        dep = departamento.encode('utf-8')
        numeroActivo = self.editNumeroActivo.text().replace(" ", "")
        foto = self.labelImagen.pixmap()

        msg = QMessageBox()
        QMessageBox().setIcon(QMessageBox.Warning)
        
        if(not  self.validaCampos()):
            msg.warning(self, "Error !", "Verifique, hay campos vacios !")
            return
        if self.validaNumeroActivo():
            msg.warning(self, "Error !", "El número de activo, ya se ha registrado !")
            self.editNumeroActivo.setFocus()
            return
        
        if foto:
            mypath = Path().absolute()
            mypath = str(mypath) + str('/imgs/activos')
            shutil.copy(self.rutaImagen, str(mypath))

        columns = 'numero, descripcion, departamento, responsable, fecha_ingreso, tag, obsoleto, imagen'
        data = " '"+numeroActivo+"', '"+descripcion+"', '"+dep+"', '"+responsble+"', '"+str(fechaIngreso)+"', '" "', "+str(0)+", '"+self.nombreImagen+"' "
        print(data)

        rowId = DB.write('activos', columns, data)

        btnRespuesta = QMessageBox.question(self, 'Información guardada correctamente', "Quiere asignar el registro a una etiqueta NFC?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if btnRespuesta == QMessageBox.Yes:
            self.SW = AsignarTagNFC(None, rowId, DB)
            self.close()
        else:
            self.volver()

    
    def validaCampos(self):
        numero = self.editNumeroActivo.text().replace(" ", "")
        responsble = self.editResponsable.text()
        descripcion = self.editDescripcion.toPlainText()
        foto = self.labelImagen.pixmap()
        validado = True
        if (not numero):
            validado = False
        if (not responsble):
            validado = False
        if (not descripcion):
            validado = False
        if (not foto):
            validado = False
        
        return validado
    
    def validaNumeroActivo(self):
        numero = self.editNumeroActivo.text().replace(" ", "")
        return self.DB.existeNumeroActivo(numero)
    
    def volver(self):
      from menu import Menu
      self.SW = Menu(None, self.DB)
      self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = NuevoActivo()
    sys.exit(app.exec_())

