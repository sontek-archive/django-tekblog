#!/usr/bin/env python
from django.core.management import execute_manager
import imp
try:
    imp.find_module('settings') # Assumed to be in the same directory.
except ImportError: # pragma: no cover
    import sys # pragma: no cover
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n" % __file__) # pragma: no cover
    sys.exit(1) # pragma: no cover

import settings

if __name__ == "__main__":
    execute_manager(settings)
