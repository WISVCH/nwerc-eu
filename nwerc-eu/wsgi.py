import os
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

os.sys.path.append(PROJECT_PATH)
os.sys.path.append('%s/..' % PROJECT_PATH)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nwerc-eu.settings")

# This application object is used by the development server
# as well as any WSGI server configured to use this file.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()