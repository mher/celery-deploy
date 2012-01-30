from __future__ import absolute_import
from __future__ import with_statement

import os
import sys

from contextlib import contextmanager
from importlib import import_module

from fabric.api import prefix, cd


@contextmanager
def virtualenv(path):
    with cd(path):
        with prefix('source bin/activate'):
            yield


def mpath(module):
    mfile = module.__file__
    return mfile[:-1] if mfile.endswith('.pyc') else mfile


def import_celeryconfig():
    "import Celery configuration module"
    CELERY_CONFIG_MODULE = os.environ.get('CELERY_CONFIG_MODULE',
                                          'celeryconfig')
    if os.getcwd() not in sys.path:
        sys.path.insert(0, os.getcwd())
    return import_module(CELERY_CONFIG_MODULE)
