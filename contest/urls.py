from django.conf.urls.defaults import *
from views import ImportView, TeamView, SendMailsView, SubscribeView, EventView, EventSubscriptionView, SendRemindersView, \
    LiveContestRegistrationView, ExportTeamsView, ExportAffiliationsView, ExportAffiliationImagesView, ExportZip, \
    ExportLiveContestTeamsView, ExportLiveContestAffiliationsView, ExportZipKey
from django.views.generic import TemplateView


urlpatterns = patterns('',
    url(r'^activities/$', EventView.as_view(), name='events'),
    url(r'^subscriptions/$', EventSubscriptionView.as_view(), name='subscriptions'),
    url(r'^activities/subscribe/(?P<person_id>\d+)/(?P<key>\w+)/$', SubscribeView.as_view(), name='subscribe'),
    url(r'^import/$', ImportView.as_view(), name='import'),
    url(r'^teams/$', TeamView.as_view(), name='teams'),
    url(r'^send_mails/$', SendMailsView.as_view(), name='send_mails'),
    url(r'^send_reminders/$', SendRemindersView.as_view(), name='send_reminders'),
    url(r'^online-contest/register/$', LiveContestRegistrationView.as_view(), name='livecontest_registration'),
    url(r'^online-contest/registration-succes/$', \
        TemplateView.as_view(template_name='contest/livecontestregistration_success.html'), \
        name='livecontest_succes'\
    ),
    
    url(r'^export/teams/$', ExportTeamsView.as_view(), name='export_teams'),
    url(r'^export/affiliations/$', ExportAffiliationsView.as_view(), name='export_affiliations'),
    url(r'^export/affiliations/images/$', ExportAffiliationImagesView.as_view(), name='export_affiliation_images'),
    url(r'^export/zip/$', ExportZip.as_view(), name='export_zip'),
    url(r'^export/zip/(?P<key>\w+)/$', ExportZipKey.as_view(), name='export_zip_key'),
    url(r'^export/livecontest/teams/$', ExportLiveContestTeamsView.as_view(), name='export_livecontest_teams'),
    url(r'^export/livecontest/affiliations/$', ExportLiveContestAffiliationsView.as_view(), name='export_livecontest_affiliations')
)