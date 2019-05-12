__author__ = 'Felix Simkovic'
__date__ = '2019-05-11'
__license__ = 'MIT License'

import collections
import logging
import os
import sys
import yaml

logger = logging.getLogger(__name__)


class DictLockedError(Exception):
    pass


class ImmutableDictMixin(object):
    _locked = False

    def lock(self):
        self._locked = True

    def unlock(self):
        self._locked = False

    @staticmethod
    def assert_lock(outer):
        def inner(*args, **kwargs):
            if args[0]._locked:
                raise DictLockedError('Cannot override value')
            return outer(*args, **kwargs)
        return inner


class Configuration(collections.UserDict, ImmutableDictMixin):

    file = os.path.join(os.path.expanduser('~'), '.taskwpomo')
    if not os.path.isfile(file):
        open(file, 'w').close()

    @ImmutableDictMixin.assert_lock
    def __setitem__(self, key, value):
        super().__setitem__(key, value)

    @ImmutableDictMixin.assert_lock
    def setdefault(self, key, value=None):
        super().setdefault(key, value=value)
        self.write()

    @ImmutableDictMixin.assert_lock
    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)

    def write(self):
        data = yaml.dump(dict(self), default_flow_style=False)
        with open(self.file, 'w') as f:
            f.write(data)

    @classmethod
    def from_default(cls):
        return cls.read_yaml(cls.file)

    @classmethod
    def read_yaml(cls, fname):
        if not os.path.isfile(fname):
            raise FileNotFoundError('Cannot find YAML file')
        with open(fname, 'r') as f:
            data = yaml.safe_load(f)
        if data is None:
            data = {}
        config = cls(**data)
        config.dir = os.path.dirname(fname)
        config.file = fname
        return config


options = Configuration.from_default()
