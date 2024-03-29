__author__ = 'Felix Simkovic'
__date__ = '2019-05-11'
__license__ = 'MIT License'

import datetime
import logging
import os

from PyQt5.Qt import QThreadPool
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QComboBox, QGridLayout, QHBoxLayout, QLabel, QPushButton, QWidget

from taskwpomo.misc import log_call
from taskwpomo.worker import Worker

log = logging.getLogger(__name__)


class MainWindow(QWidget):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller

        self._pomo_start_ts = None
        self._current_dropdown_tasks = []
        self._taskw_sel_task = None

        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        grid.setVerticalSpacing(0.5)
        self.setLayout(grid)

        self.timer_lbl = QLabel(self)
        font = QFont('Courier New')
        font.setBold(True)
        font.setPointSize(70)
        self.timer_lbl.setFont(font)
        grid.addWidget(self.timer_lbl, 0, 0, 3, 2, Qt.AlignCenter)

        self.main_btn = QPushButton('Start', self)
        self.main_btn.clicked.connect(self.on_click_main_btn)
        grid.addWidget(self.main_btn, 0, 3, 1, 1)

        self.skip_btn = QPushButton('Skip', self)
        self.skip_btn.clicked.connect(self.on_click_skip_btn)
        grid.addWidget(self.skip_btn, 1, 3, 1, 1)

        self.reset_btn = QPushButton('Reset', self)
        self.reset_btn.clicked.connect(self.on_click_reset_btn)
        grid.addWidget(self.reset_btn, 2, 3, 1, 1)

        self.dropdown = QComboBox()
        self.dropdown.setMinimumWidth(250)
        self.dropdown.setMaximumWidth(250)
        self.dropdown.currentIndexChanged.connect(self.on_change_select_task)
        grid.addWidget(self.dropdown, 4, 0, Qt.AlignCenter)

        self.complete_btn = QPushButton('Completed', self)
        self.complete_btn.clicked.connect(self.on_click_complete_btn)
        grid.addWidget(self.complete_btn, 4, 3, 1, 1)

        self.threadpool = QThreadPool()

        self.update_timer_lbl()
        self.refresh_dropdown()

    @log_call
    def on_click_main_btn(self, _):
        if self.main_btn.text() == 'Start':
            self.start_session()
        else:
            self.stop_session()

    @log_call
    def on_click_complete_btn(self, _):
        self.stop_session()
        self.controller.taskw.complete_task(self._taskw_sel_task)
        self.refresh_dropdown()

    @log_call
    def on_click_skip_btn(self, _):
        self.controller.pomo.skip()
        self.update_timer_lbl()

    @log_call
    def on_click_reset_btn(self, _):
        self.controller.pomo.reset()
        self.update_timer_lbl()

    @log_call
    def on_change_select_task(self, i):
        self._taskw_sel_task = self._current_dropdown_tasks[i]
        log.info('Changed selected task to "%s"', self._taskw_sel_task.description)

    @log_call
    def start_session(self):
        for component in [self.complete_btn, self.skip_btn, self.reset_btn, self.dropdown]:
            component.setEnabled(False)
        if self.controller.pomo.is_work_task:
            #  self.complete_btn.setEnabled(True)
            self.threadpool.start(Worker(self.controller.taskw.start_task, self._taskw_sel_task))
            self.threadpool.start(Worker(self.controller.slack.enable_dnd, n_min=self.controller.pomo.current.value // 60))
        self._pomo_start_ts = datetime.datetime.now()
        self.main_btn.setText('Stop')

    @log_call
    def stop_session(self):
        for component in [self.complete_btn, self.skip_btn, self.reset_btn, self.dropdown]:
            component.setEnabled(True)
        if self.controller.taskw.is_running:
            self.threadpool.start(Worker(self.controller.taskw.stop_task, self._taskw_sel_task))
            self.threadpool.start(Worker(self.controller.slack.disable_dnd))
        self._pomo_start_ts = None
        self.main_btn.setText('Start')

    @log_call
    def refresh_dropdown(self):
        if self._pomo_start_ts is None:
            log.info('Considering a dropdown list refresh')
            self.controller.taskw.refresh()
            new_tasks = self.controller.taskw.tasks
            if new_tasks != self._current_dropdown_tasks:
                log.info('Refreshing dropdown list')
                self._current_dropdown_tasks = new_tasks
                self.dropdown.clear()
                self.dropdown.addItems([t.description for t in self._current_dropdown_tasks])

    @log_call
    def update_timer_lbl(self):
        pomo = datetime.timedelta(seconds=self.controller.pomo.current.value)
        log.debug('Current pomodoro time: %s', pomo)
        if self._pomo_start_ts:
            pomo = (self._pomo_start_ts + pomo) - datetime.datetime.now()
        self.timer_lbl.setText("{:02}:{:02}".format(pomo.seconds // 60, pomo.seconds % 60))
        if pomo.seconds <= 0:
            self.threadpool.start(Worker(self.controller.pomo.complete))
            self.stop_session()
