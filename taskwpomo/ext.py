"""Bunch of wrappers around external dependencies."""

__author__ = 'Felix Simkovic'
__date__ = '2019-05-11'
__license__ = 'MIT License'

import logging

from slack import WebClient
from slack.errors import SlackApiError
from tasklib import TaskWarrior

from taskwpomo.misc import log_call

log = logging.getLogger(__name__)


class Slack:
    def __init__(self, token):
        self.client = WebClient(token)

    @log_call
    def disable_dnd(self):
        log.info('Stopping Slack Do-Not-Disturb Mode')
        try:
            self.client.dnd_endSnooze().validate()
        except SlackApiError as e:
            log.error('Unable to stop Slack Do-Not-Disturb mode: %s', e)

    @log_call
    def enable_dnd(self, n_min=25):
        log.info('Starting Slack Do-Not-Disturb Mode')
        try:
            self.client.dnd_setSnooze(num_minutes=n_min)
        except SlackApiError as e:
            log.error('Unable to start Slack Do-Not-Disturb mode: %s', e)


class TaskWarrior(TaskWarrior):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._active = False
        self._displayed = []
        self._selected = None

    @property
    @log_call
    def is_running(self):
        return self._active

    @property
    @log_call
    def tasks2display(self):
        self._displayed = self.tasks.pending()
        return self._displayed

    @log_call
    def complete_selected_task(self):
        self._selected.done()
        self._selected = None
        self._active = False

    @log_call
    def toggle_selected_task(self):
        if self._active:
            log.info('Stop time monitoring for task "%s"', self._selected)
            self._selected.stop()
        else:
            log.info('Start time monitoring for task "%s"', self._selected)
            self._selected.start()
        self._active = not self._active

    @log_call
    def select_task(self, pos):
        self._selected = self._displayed[pos]
        log.info('Changing task to "%s"', self._selected)

