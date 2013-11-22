from django.conf.urls import *
from views import ExportSystemZipKeyView


urlpatterns = patterns('',
                       url(r'^export-zip/(?P<key>\w+)/$', ExportSystemZipKeyView.as_view(), name='exportZip'),
)