import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget
from PyQt5.QtCore import QSize    

class AsignarTagNFC(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'ASIGNAR TAG NFC'
        self.left = 500
        self.top = 350
        self.width = 800
        self.height = 400
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        self.setWindowTitle("ACERQUE SU TAG NFC AL LECTOR") 

        centralWidget = QWidget(self)          
        self.setCentralWidget(centralWidget)   

        gridLayout = QGridLayout(self)     
        centralWidget.setLayout(gridLayout)  

        title = QLabel("ACERQUE SU TAG NFC AL LECTOR", self) 
        title.setAlignment(QtCore.Qt.AlignCenter) 
        gridLayout.addWidget(title, 0, 0)
        self.show()

    
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AsignarTagNFC()
    sys.exit(app.exec_())