
from PyQt5.QtCore import QTimer

class Timer(QTimer):
    def __init__(self, callback):
        super().__init__()
        self.timeout.connect(callback)
