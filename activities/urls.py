from django.conf.urls import *

from views import ActivityListView


urlpatterns = patterns('',
    url(r'^$', ActivityListView.as_view(), name='list'),
)