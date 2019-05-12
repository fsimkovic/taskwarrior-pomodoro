"""Do-Not-Disturb extensions."""

__author__ = 'Felix Simkovic'
__date__ = '2019-05-11'

import logging

from slack import WebClient
from tasklib import TaskWarrior

log = logging.getLogger(__name__)


class Slack:
    def __init__(self, token):
        self.client = WebClient(token)

    def disable_dnd(self):
        log.info('Stopping Slack Do-Not-Disturb Mode')
        self.client.dnd_endSnooze().validate()
        self._active = False

    def enable_dnd(self, n_min=25):
        log.info('Starting Slack Do-Not-Disturb Mode')
        self.client.dnd_setSnooze(num_minutes=n_min).validate()
        self._active = True


class TaskWarrior(TaskWarrior):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._active = False
        self._displayed = []
        self._selected = None

    @property
    def tasks2display(self):
        self._displayed = self.tasks.pending()
        return self._displayed

    def complete_selected_task(self):
        self._selected.done()
        self._selected = None
        self._active = False

    def start_selected_task(self):
        if self._active:
            log.debug('Running task detected, not starting another.')
        else:
            log.info('Start time monitoring for task "%s"', self._selected)
            self._selected.start()
            self._active = True

    def stop_selected_task(self):
        if self._active:
            log.info('Stop time monitoring for task "%s"', self._selected)
            self._selected.stop()
            self._active = False
        else:
            log.debug('No running task detected, not stopping.')

    def select_task(self, pos):
        self._selected = self._displayed[pos]
        log.info('Changing task to "%s"', self._selected)


if __name__ == '__main__':
    import time
    taskw = TaskWarrior()
    while True:
        start = time.time()
        taskw.tasks2display
        print(time.time() - start)


