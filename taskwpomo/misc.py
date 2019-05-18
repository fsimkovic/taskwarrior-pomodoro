__author__ = 'Felix Simkovic'
__date__ = '2019-05-11'
__license__ = 'MIT License'

import logging

log = logging.getLogger(__name__)


def log_call(fn):
    def inner(*args, **kwargs):
        log.debug('Function %s called with %s and %s', fn.__name__, args, kwargs)
        return fn(*args, **kwargs)
    return inner
