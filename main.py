from __future__ import annotations
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
import sys
from interface.front.StartForm import *
from typing import *

if __name__ == '__main__':
    print("Done")

    app = QApplication([])
    window = StartForm()
    window.show()
    app.exec()
