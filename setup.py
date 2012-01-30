#!/usr/bin/env python

import celerydeploy

from setuptools import setup, find_packages


setup(
    name='celerydeploy',
    version=celerydeploy.__version__,
    description='Celery deployment tool',
    author='Mher Movsisyan',
    url='https://github.com/mher/celery-deploy',
    packages=find_packages(),
    install_requires=['fabric', 'virtualenv'],
    entry_points={
        'console_scripts': [
            'celerydeploy = celerydeploy.__main__:main',
        ]
    },
    package_data={'': ['supervisord.conf']}
)
