from django.conf.urls import *

from views import ActivityListView, SubscribeView


urlpatterns = patterns('',
                       url(r'^$', ActivityListView.as_view(), name='list'),
                       url(r'^subscribe/(?P<person_id>\d+)/(?P<key>\w+)/$', SubscribeView.as_view(), name='subscribe'),
)