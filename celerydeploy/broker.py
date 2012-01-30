from __future__ import absolute_import
from __future__ import with_statement

import sys

from fabric.api import sudo, env, task, abort, puts

from .utils import import_celeryconfig


try:
    conf = import_celeryconfig()
except ImportError:
    conf = None


@task 
def install_rabbitmq():
    "install RabbitMQ server"
    if env.host and env.host != getattr(conf, 'BROKER_HOST', None):
        puts('Skipping %s non-broker host' % env.host)
        return

    if sys.platform == 'darwin':
        sudo('port install rabbitmq-server')
    elif sys.platform.startswith('linux'):
        sudo('sudo apt-get install rabbitmq-server') 
    else:
        abort('Unsupported platform: %s' % sys.platform)


@task
def setup_rabbitmq(user=None, password=None, vhost=None, access=None):
    """setup RabbitMQ server
    create a user, a virtual host and allow the user to 
    access the virtual host
    """
    user = user or getattr(conf, 'BROKER_USER', None)
    password = password or getattr(conf, 'BROKER_PASSWORD', None)
    vhost = vhost or getattr(conf, 'BROKER_VHOST', '/')
    access = access or '".*" ".*" ".*"'
    if not all((user, password)):
        abort('Please provide broker user and password')

    sudo('rabbitmqctl add_user %s %s' % (user, password))
    sudo('rabbitmqctl add_vhost %s' % vhost)
    sudo('rabbitmqctl set_permissions -p %s %s %s' % (vhost, user, access))


@task
def start_rabbitmq():
    "start RabbitMQ server"
    if env.host and env.host != getattr(conf, 'BROKER_HOST', None):
        puts('Skipping %s non-broker host' % env.host)
        return

    if sys.platform == 'darwin':
        sudo('rabbitmq-server -detached')
    elif sys.platform.startswith('linux'):
        sudo('invoke-rc.d rabbitmq-server start')
    else:
        abort('Unsupported platform: %s' % sys.platform)


@task
def stop_rabbitmq():
    "stop RabbitMQ server"
    if env.host and env.host != getattr(conf, 'BROKER_HOST', None):
        puts('Skipping %s non-broker host' % env.host)
        return

    if sys.platform == 'darwin':
        sudo('rabbitmqctl stop')
    elif sys.platform.startswith('linux'):
        sudo('invoke-rc.d rabbitmq-server stop')
    else:
        abort('Unsupported platform: %s' % sys.platform)
