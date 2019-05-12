__author__ = 'Felix Simkovic'
__date__ = '2019-05-11'
__license__ = 'MIT License'

from PyQt5.QtCore import QTimer


class Timer(QTimer):
    def __init__(self, callback):
        super().__init__()
        self.timeout.connect(callback)
