__author__ = 'Felix Simkovic'
__date__ = '2019-05-11'
__license__ = 'MIT License'

import logging

from slack import WebClient
from slack.errors import SlackApiError

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
