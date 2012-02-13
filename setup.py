#!/usr/bin/env python
import os
import re

from setuptools import setup, find_packages


version = re.compile(r'VERSION\s*=\s*\((.*?)\)')


def get_package_version():
    "returns package version without importing it"
    base = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(base, "celerydeploy/__init__.py")) as initf:
        for line in initf:
            m = version.match(line.strip())
            if not m:
                continue
            return ".".join(m.groups()[0].split(", "))


setup(
    name='celerydeploy',
    version=get_package_version(),
    description='Celery deployment tool',
    long_description=open('README.rst').read(),
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
