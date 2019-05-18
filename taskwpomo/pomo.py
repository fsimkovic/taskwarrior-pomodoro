__author__ = 'Felix Simkovic'
__date__ = '2019-05-11'
__license__ = 'MIT License'

import datetime
import enum
import logging
import time

from taskwpomo.misc import log_call

log = logging.getLogger(__name__)


@enum.unique
class PomodoroTimes(enum.Enum):
    LONG_BREAK = 1_200
    SHORT_BREAK = 300
    WORK = 1_500


class Pomodoro:

    # Steps as outlined in: 
    #   https://en.wikipedia.org/wiki/Pomodoro_Technique#Underlying_principles
    STEPS = (
        PomodoroTimes.WORK,
        PomodoroTimes.SHORT_BREAK,
        PomodoroTimes.WORK,
        PomodoroTimes.SHORT_BREAK,
        PomodoroTimes.WORK,
        PomodoroTimes.SHORT_BREAK,
        PomodoroTimes.WORK,
        PomodoroTimes.SHORT_BREAK,
        PomodoroTimes.WORK,
        PomodoroTimes.LONG_BREAK,
    )

    def __init__(self):
        self._cur_index = 0

    @property
    def completed(self):
        return self._cur_index == len(self.STEPS)

    @property
    def current(self):
        return self.STEPS[self._cur_index]

    @property
    def is_work_task(self):
        return self.current in (PomodoroTimes.WORK, )

    @property
    def next(self):
        if self._cur_index < len(self.STEPS) - 1:
            return self.STEPS[self._cur_index + 1]

    @log_call
    def complete(self):
        if self._cur_index < len(self.STEPS) - 1:
            self._cur_index += 1
        else:
            self.reset()

    @log_call
    def reset(self):
        self._cur_index = 0

    @log_call
    def skip(self):
        self.complete()

