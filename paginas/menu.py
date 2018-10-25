
from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFrame, QLabel, QComboBox, QLineEdit,
                             QPushButton)

class Menu(QMainWindow):
    def __init__(self):
      super(Menu, self).__init__()
      self.setWindowTitle("HOME")
      self.setWindowIcon(QIcon("icono.png"))
      self.setWindowFlags(Qt.WindowCloseButtonHint |
                          Qt.MSWindowsFixedSizeDialogHint)
      self.setFixedSize(400, 380)

      paleta = QPalette()
      paleta.setColor(QPalette.Background, QColor(243, 243, 243))
      self.setPalette(paleta)

      lbl = QLabel('MENU>>>>>', self)


if __name__ == '__main__':
    
    import sys
    
    aplicacion = QApplication(sys.argv)

    fuente = QFont()
    fuente.setPointSize(10)
    fuente.setFamily("Bahnschrift Light")

    aplicacion.setFont(fuente)
    
    ventana = Menu()
    ventana.show()
    
    sys.exit(aplicacion.exec_())