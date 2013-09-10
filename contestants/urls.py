from django.conf.urls import *
from contestants.views import TeamListView


urlpatterns = patterns('',
                       url(r'^$', TeamListView.as_view(), name='list'),
)