from __future__ import absolute_import

import os
import sys

from fabric.state import env
from fabric.main import main as fabric_main

import celerydeploy

env.use_ssh_config = True

def main():
    fabfile = os.path.join(celerydeploy.__path__[0], '__init__.py')
    sys.argv = ['fab', '-f', fabfile] + sys.argv[1:]
    fabric_main()

if __name__ == "__main__":
    main()
