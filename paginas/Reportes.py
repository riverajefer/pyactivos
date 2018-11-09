#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, subprocess
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QHBoxLayout, 
QGroupBox, QDialog, QVBoxLayout, QGridLayout, QGridLayout, QLabel, QHeaderView,
QMainWindow, QTableWidget,QTableWidgetItem)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from xlsxwriter.workbook import Workbook
workbook = Workbook('reporte.xlsx')
worksheet = workbook.add_worksheet()

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
        self.layoutTabla = QVBoxLayout()
        self.layoutGrid = QGridLayout()
        self.lblTitulo = QLabel('REPORTE')
        self.lblTitulo.setStyleSheet("QLabel {font-weight: bold;}")

        btnAbrirReporte = QPushButton("ABRIR REPORTE", self)
        btnAbrirReporte.setFixedWidth(135)
        btnAbrirReporte.setFixedHeight(35)
        btnAbrirReporte.clicked.connect(self.abrirReporte)

        btnVolver = QPushButton("VOLVER", self) 
        btnVolver.setFixedWidth(180)
        btnVolver.setFixedHeight(35)        
        btnVolver.clicked.connect(self.volver)        
        btnVolver.move(200,300)

        self.layoutTabla.addWidget(self.lblTitulo) 
        self.layoutTabla.addWidget(self.tableWidget) 
        self.layoutTabla.addWidget(btnAbrirReporte) 
        self.layoutTabla.addWidget(btnVolver) 
        self.setLayout(self.layoutTabla) 
        #self.show()
        self.showFullScreen()

    def createTable(self):
        # Create table
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["Usuario", "Activo", "Fecha de consulta"])
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)       
        header.setSectionResizeMode(2, QHeaderView.Stretch)

        worksheet.set_header("&CHere is some centered text.")

        rowReportes = self.DB.reportes(1)
        for row in rowReportes:
            inx = rowReportes.index(row)
            self.tableWidget.insertRow(inx)
            self.tableWidget.setItem(inx, 0, QTableWidgetItem(row[0]))
            self.tableWidget.setItem(inx, 1, QTableWidgetItem(row[1]))
            self.tableWidget.setItem(inx, 2, QTableWidgetItem(row[2]))

            worksheet.write(inx+1, 0, row[0])
            worksheet.write(inx+1, 1, row[1])
            worksheet.write(inx+1, 2, row[2])

        worksheet.write(0, 0, 'Nombre')
        worksheet.write(0, 1, 'Activo')
        worksheet.write(0, 2, 'Fecha de consulta')
        self.tableWidget.move(0,0)
        workbook.close()
    
    def abrirReporte(self):
        if sys.platform == "win32":
            os.startfile('reporte.xlsx')
        else:
            opener ="open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, 'reporte.xlsx'])        
        
 
    def volver(self):
      from menu import Menu
      self.SW = Menu(None, self.DB)
      self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Reportes()
    sys.exit(app.exec_())