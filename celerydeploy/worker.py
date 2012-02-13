from __future__ import absolute_import
from __future__ import with_statement

import os

from importlib import import_module

from fabric.api import run, env, put, task, require, puts

from .utils import virtualenv, mpath, import_celeryconfig


@task
def setup():
    """setup virtual environments for workers
    create a virtual environment, install required packages"""
    require('celery_path')
    run('virtualenv %s' % env.celery_path)
    with virtualenv(env.celery_path):
        run('pip install celery')
        run('pip install supervisor')


@task
def start():
    """run workers
    create supervisord.conf file in the current directory if you need
    to change the default configuration"""
    require('celery_path')
    with virtualenv(env.celery_path):
        sconf = 'supervisord.conf'
        if not os.path.exists(sconf):
            sconf = os.path.join(os.path.dirname(__file__), sconf)

        put(sconf, '.')
        run('supervisord -c supervisord.conf')


@task
def stop():
    "stop workers"
    require('celery_path')
    with virtualenv(env.celery_path):
        run('supervisorctl -c supervisord.conf stop celeryd')
        run('supervisorctl -c supervisord.conf shutdown')


@task
def restart():
    "restart workers"
    require('celery_path')
    with virtualenv(env.celery_path):
        run('supervisorctl -c supervisord.conf restart celeryd')


@task
def deploy():
    "deploy modules listed in CELERY_IMPORTS"
    require('celery_path')
    with virtualenv(env.celery_path):
        conf = import_celeryconfig()
        put(mpath(conf), '.')
        for module in map(import_module, conf.CELERY_IMPORTS):
            put(mpath(module), '.')


@task
def start_celerybeat(host=None):
    "start celerybeat scheduler"
    host = host or env.hosts[0]
    conf = import_celeryconfig()
    if env.host and env.host != host:
        puts('Skipping %s non-beat host' % env.host)
        return

    if getattr(conf, 'CELERYBEAT_SCHEDULE', None):
        require('celery_path')
        with virtualenv(env.celery_path):
            run('supervisorctl -c supervisord.conf start celerybeat')


@task
def stop_celerybeat(host=None):
    "stop celerybeat scheduler"
    host = host or env.hosts[0]
    conf = import_celeryconfig()
    if env.host and env.host != host:
        puts('Skipping %s non-beat host' % env.host)
        return

    if getattr(conf, 'CELERYBEAT_SCHEDULE', None):
        require('celery_path')
        with virtualenv(env.celery_path):
            run('supervisorctl -c supervisord.conf stop celerybeat')
