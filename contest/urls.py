from django.conf.urls.defaults import *
from views import ImportView, TeamView, SendMailsView, SubscribeView, EventView, EventSubscriptionView


urlpatterns = patterns('',
    url(r'^activities/$', EventView.as_view(), name='events'),
    url(r'^subscriptions/$', EventSubscriptionView.as_view(), name='subscriptions'),
    url(r'^activities/subscribe/(?P<person_id>\d+)/(?P<key>\w+)/$', SubscribeView.as_view(), name='subscribe'),
    url(r'^import/$', ImportView.as_view(), name='import'),
    url(r'^teams/$', TeamView.as_view(), name='teams'),
    url(r'^send_mails/$', SendMailsView.as_view(), name='send_mails')
)