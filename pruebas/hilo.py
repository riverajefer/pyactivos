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


class Thread(QThread):

    def __init__(self, parent):
        QThread.__init__(self, parent)

        self.window = parent

        self._lock = threading.Lock()
        self.running = False

    def stop(self):
        self.running = False
        print('received stop signal from window.')
        with self._lock:
            self._do_before_done()

    def _do_work(self):
        print('thread is running...')
        self.sleep(1)

    def _do_before_done(self):
        print('waiting 3 seconds before thread done..')
        for i in range(3, 0, -1):
            print('{0} seconds left...'.format(i))
            self.sleep(1)
        print('ok, thread done.')

    def run(self):
        self.running = True
        while self.running:
            with self._lock:
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