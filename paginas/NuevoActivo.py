import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout, QMainWindow, QLabel, QLineEdit, QTextEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
 
class NuevoActivo(QDialog):
    def __init__(self):
        super().__init__()
        self.title = 'MENÚ'
        self.left = 500
        self.top = 350
        self.width = 800
        self.height = 400        
        
        self.initUI()
        
        
    def initUI(self):
        
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        title = QLabel('Title')
        author = QLabel('Author')
        review = QLabel('Review')
        nomero = QLabel('numero')

        titleEdit = QLineEdit()
        authorEdit = QLineEdit()
        reviewEdit = QTextEdit()
        numeroEdit = QLineEdit()

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(title, 1, 0)
        grid.addWidget(titleEdit, 1, 1)

        grid.addWidget(author, 2, 0)
        grid.addWidget(authorEdit, 2, 1)

        grid.addWidget(review, 3, 0)
        grid.addWidget(reviewEdit, 3, 1, 5, 1)
        
        grid.addWidget(nomero, 1, 2)
        grid.addWidget(numeroEdit, 1, 3)

        self.setLayout(grid) 
        
        
        self.show()
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = NuevoActivo()
    sys.exit(app.exec_())