__author__ = 'Felix Simkovic'
__date__ = '2019-05-11'
__license__ = 'MIT License'

import datetime
import logging
import unittest.mock

from taskwpomo.config import options
from taskwpomo.slacky import Slack
from taskwpomo.taskw import TaskWarrior
from taskwpomo.pomo import Pomodoro

log = logging.getLogger(__name__)


class MainController:
    def __init__(self):
        log.info('Initialising new %s', self.__class__.__name__)

        self.pomo = Pomodoro()
        self.taskw = TaskWarrior()
        if 'slack-token' in options:
            self.slack = Slack(token=options['slack-token'])
        else:
            self.slack = unittest.mock.Mock()
