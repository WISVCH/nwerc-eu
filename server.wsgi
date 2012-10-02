import os
import sys

path = '/srv/www/commissies/chipcie/nwerc-eu'
if path not in sys.path:
    sys.path.append(path)
    sys.path.append(os.path.normpath(path+"/src"))

os.environ['DJANGO_SETTINGS_MODULE'] = 'src.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()