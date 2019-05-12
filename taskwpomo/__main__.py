__author__ = 'Felix Simkovic'
__date__ = '2019-05-11'
__license__ = 'MIT License'

import logging
import sys

from PyQt5.QtWidgets import QApplication

from taskwpomo import APPLICATION_NAME
from taskwpomo.timer import Timer
from taskwpomo.window import MainWindow

logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setApplicationName(APPLICATION_NAME)

    window = MainWindow()
    window.show()

    t1 = Timer(window.refresh_dropdown)
    t1.start(1000)
    t2 = Timer(window.update_timer_lbl)
    t2.start(1000)

    sys.exit(app.exec_())
