from __future__ import absolute_import
from __future__ import with_statement

from fabric.api import run, env, task, require

from celerydeploy import broker
from celerydeploy import worker

from celerydeploy.utils import virtualenv, import_celeryconfig


VERSION = (0, 2, 0)

__version__ = '.'.join(map(str, VERSION))

try:
    conf = import_celeryconfig()
except ImportError:
    pass
else:
    if hasattr(conf, 'CELERY_DEPLOY_PATH'):
        env['celery_path'] = conf.CELERY_DEPLOY_PATH
    if not env.hosts and hasattr(conf, 'CELERY_DEPLOY_HOSTS'):
        env['hosts'] = conf.CELERY_DEPLOY_HOSTS


@task
def version():
    "print version info"
    require('celery_path')
    with virtualenv(env.celery_path):
        run('python -V')
        run('python -c "import celery;print(celery.__version__)"')
        run('python -c "import kombu;print(kombu.__version__)"')
