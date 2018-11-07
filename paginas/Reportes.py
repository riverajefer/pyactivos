#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QHBoxLayout, 
QGroupBox, QDialog, QVBoxLayout, QGridLayout, 
QMainWindow, QTableWidget,QTableWidgetItem)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

class Reportes(QDialog):
    def __init__(self, parent=None, DB=None):
        super(Reportes, self).__init__(parent)
        self.title = 'REPORTE'
        self.left = 500
        self.top = 350
        self.width = 800
        self.height = 400
        self.DB = DB
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createTable()
 
        # Add box layout, add table to box layout and add box layout to widget
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget) 
        self.setLayout(self.layout) 
 
        # Show widget
        self.show()

    def createTable(self):
        # Create table
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(4)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["Usuario", "Activo", "Fecha"])

        rowReportes = self.DB.reportes(1)
        for row in rowReportes:
            inx = rowReportes.index(row)
            print(row)
            print(row[1])
            self.tableWidget.insertRow(inx)
            self.tableWidget.setItem(inx, 0, QTableWidgetItem(row[0]))
            self.tableWidget.setItem(inx, 1, QTableWidgetItem(row[1]))
            self.tableWidget.setItem(inx, 2, QTableWidgetItem(row[2]))

        self.tableWidget.move(0,0)
        # table selection change
 
     
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Reportes()
    sys.exit(app.exec_())