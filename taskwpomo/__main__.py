__author__ = 'Felix Simkovic'
__date__ = '2019-05-11'
__license__ = 'MIT License'

import argparse
import logging
import sys

from PyQt5.QtWidgets import QApplication

from taskwpomo import APPLICATION_NAME
from taskwpomo.timer import Timer
from taskwpomo.window import MainWindow

FORMAT = "[%(asctime)-15s|%(module)s|%(lineno)d] %(levelname)s - %(message)s"


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--debug', action='store_true')
    args = p.parse_args()

    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=log_level, format=FORMAT)

    app = QApplication([])
    app.setApplicationName(APPLICATION_NAME)
    window = MainWindow()
    window.show()

    t1 = Timer(window.refresh_dropdown)
    t1.start(5000)
    t2 = Timer(window.update_timer_lbl)
    t2.start(1000)

    sys.exit(app.exec_())
