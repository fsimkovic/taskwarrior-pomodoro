__author__ = 'Felix Simkovic'
__date__ = '2019-05-11'
__license__ = 'MIT License'

import datetime
import logging
import os
import unittest.mock

from PyQt5.QtCore import Qt
from PyQt5.QtMultimedia import QSound
from PyQt5.QtWidgets import QComboBox, QGridLayout, QHBoxLayout, QLabel, QPushButton, QWidget

from taskwpomo.config import options
from taskwpomo.ext import Slack, TaskWarrior
from taskwpomo.pomo import Pomodoro

log = logging.getLogger(__name__)

READY_SOUND = os.path.join(os.path.dirname(__file__), 'data', 'ding.wav')


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.pomo = Pomodoro()
        if 'slack-token' in options:
            self.slack = Slack(token=options['slack-token'])
        else:
            self.slack = unittest.mock.Mock()
        self.taskw = TaskWarrior()

        # TODO: refactor this logic out of here
        self._pomo_start_ts = None
        self._chime = QSound(READY_SOUND)

        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        grid.setVerticalSpacing(0.5)
        self.setLayout(grid)

        self.timer_lbl = QLabel(self)
        font = self.timer_lbl.font()
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
        self.dropdown.currentIndexChanged.connect(self.taskw.select_task)
        grid.addWidget(self.dropdown, 4, 0, Qt.AlignCenter)

        self.complete_btn = QPushButton('Completed', self)
        self.complete_btn.clicked.connect(self.on_click_complete_btn)
        grid.addWidget(self.complete_btn, 4, 3, 1, 1)

        self.update_timer_lbl()
        self.refresh_dropdown()

    def on_click_main_btn(self):
        if self.main_btn.text() == 'Start':
            self.start_session()
        else:
            self.stop_session()

    def on_click_complete_btn(self):
        self.stop_session()
        self.taskw.complete_selected_task()

    def on_click_skip_btn(self):
        log.info('Skip pomodoro session')
        self.pomo.skip()
        self.update_timer_lbl()

    def on_click_reset_btn(self):
        log.info('Reset pomodoro sequence')
        self.pomo.reset()
        self.update_timer_lbl()

    def start_session(self):
        for component in [self.complete_btn, self.skip_btn, self.reset_btn, self.dropdown]:
            component.setEnabled(False)
        if self.pomo.is_work_task:
            self.complete_btn.setEnabled(True)
            self.taskw.start_selected_task()
            self.slack.enable_dnd()
        self._pomo_start_ts = datetime.datetime.now()
        self.main_btn.setText('Stop')

    def stop_session(self):
        for component in [self.complete_btn, self.skip_btn, self.reset_btn, self.dropdown]:
            component.setEnabled(True)
        if self.taskw.is_running:
            self.taskw.stop_selected_task()
            self.slack.disable_dnd()
        self._pomo_start_ts = None
        self.main_btn.setText('Start')

    def refresh_dropdown(self):
        # TODO: this is super hacky, we must be able to do better
        displayed = set(); i = 0
        while True:
            value = self.dropdown.itemText(i).strip()
            if value:
                displayed.add(value); i += 1
            else:
                break

        labels = [str(t) for t in self.taskw.tasks2display]
        if self._pomo_start_ts is None and set(labels) != displayed:
            self.dropdown.clear()
            self.dropdown.addItems(labels)
            self.dropdown.setCurrentIndex(0)

    def update_timer_lbl(self):
        pomo = datetime.timedelta(seconds=self.pomo.current.value)
        log.debug('Current pomodoro time: %s', pomo)
        if self._pomo_start_ts:
            pomo = (self._pomo_start_ts + pomo) - datetime.datetime.now()
        if pomo.seconds > 0:
            self.timer_lbl.setText("{:02}:{:02}".format(pomo.seconds // 60, pomo.seconds % 60))
        else:
            self.pomo.complete()
            self.stop_session()
            self._chime.play()
