from django.conf.urls import *
from django.views.generic import TemplateView
from livecontest.views import RegistrationView


urlpatterns = patterns('',
                       url(r'^registration/$', RegistrationView.as_view(), name='livecontest-register'),
                       url(r'^registration/success/$',
                           TemplateView.as_view(template_name='livecontest/success.html'),
                           name='livecontest-success'),
)