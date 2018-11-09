import threading

import sys
from sys import platform
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QHBoxLayout, 
QGroupBox, QDialog, QVBoxLayout, 
QGridLayout, QMainWindow, QLabel, QLineEdit, QMessageBox)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, QThread, pyqtSignal
from threading import Thread
import signal
import subprocess
import time
import datetime

try:
    import nfc
except ImportError:
    pass


class Thread(QThread):

    def __init__(self, parent):
        QThread.__init__(self, parent)

        self.window = parent

        try:
            self.clf = nfc.ContactlessFrontend('usb')
        except Exception as err:
           print('Error NFC dispositivo')

        self._lock = threading.Lock()
        self.running = False

    def stop(self):
        self.running = False
        print('received stop signal from window.')
        self.clf.close()

    def finNFC(self):
        return self.running
        


    def _do_work(self):
        print('thread is running...')
        tag = self.clf.connect(rdwr={'on-connect': lambda tag: False}, terminate=self.finNFC)
        try:
            self.tag_id = tag.identifier.encode('hex')
            print(self.tag_id)
            self.signal.emit(self.tag_id)
            self.clf.close()
        except Exception:
            print('terminado por tiempo')
            self.clf.close()        


    def run(self):
        self.running = True
        while self.running:
            self._do_work()


class Window(QMainWindow):

    def __init__(self, app):
        # remember:
        # do not bind QApplication instance `app` to attribute of any object,
        # e.g self.app = app,
        # that will cause segmentation fault due to gc when closing.
        QMainWindow.__init__(self)
        self.setMinimumSize(QSize(300, 200)) 
        pybutton = QPushButton('Click me', self)
        pybutton.clicked.connect(self.clickMethod)
        pybutton.resize(100,32)
        pybutton.move(50, 50)

        self.thread = Thread(self)
        app.aboutToQuit.connect(self.thread.stop)
        self.thread.start()

    
    def clickMethod(self):
        print('Clicked Pyqt button. STOP THREAD')
        self.thread.stop()



if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = Window(app)
    window.show()
    sys.exit(app.exec_())