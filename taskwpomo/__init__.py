__author__ = 'Felix Simkovic'
__date__ = '2019-05-11'
__license__ = 'MIT License'

import os
import sys

APPLICATION_NAME = 'Pomodoro TaskWarrior'


if sys.platform.startswith('darwin'):
    try:
        from Foundation import NSBundle
        bundle = NSBundle.mainBundle()
        if bundle:
            app_info = bundle.localizedInfoDictionary() or bundle.infoDictionary()
            if app_info:
                app_info['CFBundleName'] = APPLICATION_NAME
    except ImportError:
        pass
