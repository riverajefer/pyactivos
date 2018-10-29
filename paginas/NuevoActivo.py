import sys
from os import getcwd, path
import os
import shutil
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QHBoxLayout, 
QGroupBox, QDialog, QVBoxLayout, QGridLayout, 
QMainWindow, QLabel, QLineEdit, QTextEdit,
QComboBox, QCalendarWidget, QFileDialog)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot, QDate, Qt, pyqtSignal, QByteArray, QIODevice, QBuffer
from pathlib import Path
sys.path.append('..')
from DB.database import Database

db_path = 'db.db'
DB = Database()
DB.open(db_path)

class QLabelClickable(QLabel):
    clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super(QLabelClickable, self).__init__(parent)

    def mousePressEvent(self, event):
        self.clicked.emit()    

class NuevoActivo(QDialog):
    def __init__(self):
        super().__init__()
        self.title = 'MENÚ'
        self.left = 500
        self.top = 350
        self.width = 800
        self.height = 400        
        self.initUI()
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
        self.comboDepartamento.setCurrentIndex(1)
        self.comboDepartamento.setFixedWidth(self.widthtInput)
        self.comboDepartamento.setFixedHeight(self.heightInput)

        self.editNumeroActivo = QLineEdit()
        self.editNumeroActivo.setFixedWidth(self.widthtInput)
        self.editNumeroActivo.setFixedHeight(self.heightInput)

        self.editResponsable = QLineEdit()
        self.editResponsable.setFixedWidth(self.widthtInput)
        self.editResponsable.setFixedHeight(self.heightInput)

        self.cal = QCalendarWidget(self)
        self.cal.setGridVisible(True)
        self.cal.setFixedWidth(350)
        self.cal.setFixedHeight(200)
        self.cal.clicked[QDate].connect(self.showDate)


        self.editDescripcion = QTextEdit()

        grid = QGridLayout()
        grid.setSpacing(15)

        grid.addWidget(lblNumeroActivo, 0, 0)
        grid.addWidget(self.editNumeroActivo, 1, 0)

        grid.addWidget(lblResponsable, 2, 0)
        grid.addWidget(self.editResponsable, 3, 0)

        grid.addWidget(lblDepartamento, 4, 0)
        grid.addWidget(self.comboDepartamento, 5, 0)

        grid.addWidget(lblFechaIngreso, 6, 0)
        grid.addWidget(self.cal, 7, 0)

        grid.addWidget(lblDescripcion, 0, 1)
        grid.addWidget(self.editDescripcion, 1, 1, 3, 1)

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
        self.btnGuardar.setFixedWidth(150)
        self.btnGuardar.setFixedHeight(50)        
        self.btnGuardar.clicked.connect(self.guardar)


        grid.addWidget(self.labelImagen, 6, 1, 3, 3)
        grid.addWidget(self.btnSeleccionar, 6, 1)
        grid.addWidget(self.btnGuardar, 7, 2)

        self.setLayout(grid) 
        self.show()

    def showDate(self, date):
        print(date.toString())        
        self.fechaIngreso = date.toString();
 
    def seleccionarImagen(self):
        self.rutaImagen, extension = QFileDialog.getOpenFileName(self, "Seleccionar imagen", getcwd(),
                                                        "Archivos de imagen (*.png *.jpg)",
                                                        options=QFileDialog.Options())
        
        print(self.rutaImagen)
        self.nombreImagen = path.basename(self.rutaImagen)

        if self.rutaImagen:
            # Adaptar imagen
            pixmapImagen = QPixmap(self.rutaImagen).scaled(180, 180, Qt.KeepAspectRatio,
                                                  Qt.SmoothTransformation)

            # Mostrar imagen
            self.labelImagen.setPixmap(pixmapImagen)
    
    def guardar(self):
        print('Guardar...')
        #numeroActivo = self.editNumeroActivo.text()
        responsble = self.editResponsable.text()
        descripcion = self.editDescripcion.toPlainText()
        departamento = self.comboDepartamento.currentText()

        numeroActivo = " ".join(self.editNumeroActivo.text().split()).title()
        foto = self.labelImagen.pixmap() 
        
        if foto:
            mypath = Path().absolute()
            mypath = str(mypath) + str('/imgs/activos')

            shutil.copy(self.rutaImagen, str(mypath))
  

        print('numero: ', numeroActivo)
        print('fecha: ', self.fechaIngreso)
        print('foto: ', foto)
        print('Ruta imagen: ', self.rutaImagen)
        print('nombre imagen: ', self.nombreImagen)

        columns = 'numero, descripcion, departamento, responsable, fecha_ingreso, tag, obsoleto, imagen'
        data = " '"+numeroActivo+"', '"+descripcion+"', '"+departamento+"', '"+responsble+"', '"+str(self.fechaIngreso)+"', '" "', "+str(0)+", '"+self.nombreImagen+"' "
        print(data)

        DB.write('activos', columns, data)
        print('OK escrito !')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = NuevoActivo()
    sys.exit(app.exec_())

