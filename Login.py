#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
El módulo *login* tiene como objetivo mostrar la forma de crear una ventana de login
sencilla.
"""
from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, qApp, QFrame, QLabel, QComboBox, QLineEdit,
                             QPushButton, QMessageBox)

from paginas.menu import Menu
from DB.database import Database
from sys import platform

db_path = 'db.db'
DB = Database()
DB.open(db_path)

# ===================== CLASE ventanaLogin =========================

class ventanaLogin(QMainWindow):
  def __init__(self, parent=None):
    super(ventanaLogin, self).__init__(parent)
    
    self.setWindowTitle("Login")
    self.setWindowIcon(QIcon("app.png"))
    self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint)
    self.setFixedSize(800, 480)

    paleta = QPalette()
    paleta.setColor(QPalette.Background, QColor(243, 243, 243))
    self.setPalette(paleta)

    self.initUI()

  def initUI(self):
    self.menuTop()
    self.encabezado()
    self.formulario_login()

  def menuTop(self):
    exitAct = QAction(QIcon('salir.png'), '&SALIR', self)        
    exitAct.setShortcut('Ctrl+Q')
    exitAct.setStatusTip('Salir de la aplicación')
    exitAct.triggered.connect(qApp.quit)
    self.statusBar()
    menubar = self.menuBar()
    fileMenu = menubar.addMenu('&Archivo')
    fileMenu.addAction(exitAct)
  
  def encabezado(self):
    paleta = QPalette()
    paleta.setColor(QPalette.Background, QColor(51, 0, 102))

    frame = QFrame(self)
    frame.setFrameShape(QFrame.NoFrame)
    frame.setFrameShadow(QFrame.Sunken)
    frame.setAutoFillBackground(True)
    frame.setPalette(paleta)
    frame.setFixedWidth(800)
    frame.setFixedHeight(84)
    frame.move(0, 25)

    labelIcono = QLabel(frame)
    labelIcono.setFixedWidth(40)
    labelIcono.setFixedHeight(40)
    labelIcono.setPixmap(QPixmap("icono.png").scaled(40, 40, Qt.KeepAspectRatio,
                                                      Qt.SmoothTransformation))
    labelIcono.move(37, 22)

    fuenteTitulo = QFont()
    fuenteTitulo.setPointSize(16)
    fuenteTitulo.setBold(True)

    labelTitulo = QLabel("<font color='white'>NFC</font>", frame)
    labelTitulo.setFont(fuenteTitulo)
    labelTitulo.move(83, 20)

    fuenteSubtitulo = QFont()
    fuenteSubtitulo.setPointSize(9)

    labelSubtitulo = QLabel("<h2><font color='white'>Sistema de control de activos fijos "
                            "(Python).</font></h2>", frame)
    labelSubtitulo.setFont(fuenteSubtitulo)
    labelSubtitulo.move(83, 46)

  def formulario_login(self):
    # =================== WIDGETS LOGIN ======================
    labelCuenta = QLabel("Cuenta", self)
    labelCuenta.move(260, 110)

    self.comboBoxCuenta = QComboBox(self)
    self.comboBoxCuenta.addItems(["Administrador", "Usuario"])
    self.comboBoxCuenta.setCurrentIndex(1)
    self.comboBoxCuenta.setFixedWidth(280)
    self.comboBoxCuenta.setFixedHeight(26)
    self.comboBoxCuenta.move(260, 136)

    # ========================================================
    labelUsuario = QLabel("Usuario", self)
    labelUsuario.move(260, 170)

    frameUsuario = QFrame(self)
    frameUsuario.setFrameShape(QFrame.StyledPanel)
    frameUsuario.setFixedWidth(280)
    frameUsuario.setFixedHeight(28)
    frameUsuario.move(260, 196)

    imagenUsuario = QLabel(frameUsuario)
    imagenUsuario.setPixmap(QPixmap("imgs/user.png").scaled(20, 20, Qt.KeepAspectRatio,
                                                          Qt.SmoothTransformation))
    imagenUsuario.move(10, 4)

    self.lineEditUsuario = QLineEdit(frameUsuario)
    self.lineEditUsuario.setFrame(False)
    self.lineEditUsuario.setTextMargins(8, 0, 4, 1)
    self.lineEditUsuario.setFixedWidth(238)
    self.lineEditUsuario.setFixedHeight(26)
    self.lineEditUsuario.move(40, 1)
    self.lineEditUsuario.setText('admin')

    # ========================================================

    labelContrasenia = QLabel("Contraseña", self)
    labelContrasenia.move(260, 224)

    frameContrasenia = QFrame(self)
    frameContrasenia.setFrameShape(QFrame.StyledPanel)
    frameContrasenia.setFixedWidth(280)
    frameContrasenia.setFixedHeight(28)
    frameContrasenia.move(260, 250)

    imagenContrasenia = QLabel(frameContrasenia)
    imagenContrasenia.setPixmap(QPixmap("imgs/lock").scaled(20, 20, Qt.KeepAspectRatio,
                                                                  Qt.SmoothTransformation))
    imagenContrasenia.move(10, 4)

    self.lineEditContrasenia = QLineEdit(frameContrasenia)
    self.lineEditContrasenia.setFrame(False)
    self.lineEditContrasenia.setEchoMode(QLineEdit.Password)
    self.lineEditContrasenia.setTextMargins(8, 0, 4, 1)
    self.lineEditContrasenia.setFixedWidth(238)
    self.lineEditContrasenia.setFixedHeight(26)
    self.lineEditContrasenia.move(40, 1)
    self.lineEditContrasenia.setText('123')

    #================== WIDGETS QPUSHBUTTON ===================

    buttonLogin = QPushButton("Iniciar sesión", self)
    buttonLogin.setFixedWidth(135)
    buttonLogin.setFixedHeight(28)
    buttonLogin.move(260, 286)

    buttonCancelar = QPushButton("Salir", self)
    buttonCancelar.setFixedWidth(135)
    buttonCancelar.setFixedHeight(28)
    buttonCancelar.move(400, 286)

    #==================== MÁS INFORMACIÓN =====================

    labelInformacion = QLabel("<a href='#'>Más información</a>.", self)
    labelInformacion.setOpenExternalLinks(True)
    labelInformacion.setToolTip("Jefferson y Jonathan")
    labelInformacion.move(15, 344)

    #==================== SEÑALES BOTONES =====================

    buttonLogin.clicked.connect(self.login)
    buttonCancelar.clicked.connect(self.close)             

  def login(self):
    cuenta = self.comboBoxCuenta.currentText()
    usuario = self.lineEditUsuario.text()
    password = self.lineEditContrasenia.text()

    user_id = DB.login(usuario, password)
    
    if (user_id):
      self.SW = Menu(None, DB)
      self.SW.show()
      
      self.actualizarSesion(user_id)

      self.close()
      self.limpiar_campos()
    else:
      self.mesgError()
      self.limpiar_campos()

  
  def mesgError(self):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.warning(self, "Mensaje !", "Datos incorrectos")
        
  def limpiar_campos(self):
    self.lineEditUsuario.clear()
    self.lineEditContrasenia.clear()          

  def actualizarSesion(self, user_id):
    DB.actualizarSession(user_id)
  
    
# ================================================================

if __name__ == '__main__':
    
  import sys
  
  aplicacion = QApplication(sys.argv)

  fuente = QFont()
  fuente.setPointSize(10)
  fuente.setFamily("Bahnschrift Light")
  aplicacion.setFont(fuente)
  
  ventana = ventanaLogin()

  if platform == "linux" or platform == "linux2":
    ventana.showFullScreen()
  else:
    ventana.show()
  
  sys.exit(aplicacion.exec_())
