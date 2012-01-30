#!/usr/bin/env python

import os
import celerydeploy

from setuptools import setup, find_packages


def abspath(fname):
    return os.path.join(os.path.dirname(__file__), fname)


setup(
    name='celerydeploy',
    version=celerydeploy.__version__,
    description='Celery deployment tool',
    author='Mher Movsisyan',
    packages=find_packages(),
    install_requires=['fabric', 'virtualenv'],
    entry_points={
        'console_scripts': [
            'celerydeploy = celerydeploy.__main__:main',
        ]
    },
    data_files=[('etc', map(abspath, ['celerydeploy/supervisord.conf']))]
)
