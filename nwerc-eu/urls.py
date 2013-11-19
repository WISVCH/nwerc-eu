from django.conf.urls import *
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.conf import settings
from tastypie.api import Api
from system.api import ComputerResource, TeamPlacementResource
from contestants.api import TeamResource, CountryResource, InstitutionResource

v1_api = Api(api_name='v1')
v1_api.register(ComputerResource())
v1_api.register(TeamPlacementResource())
v1_api.register(TeamResource())
v1_api.register(CountryResource())
v1_api.register(InstitutionResource())


admin.autodiscover()

urlpatterns = i18n_patterns('',
                            url(r'^admin/', include(admin.site.urls)),
                            (r'^api/', include(v1_api.urls)),
                            # url(r'^contest/', include('contest.urls')),
                            url(r'^', include('cms.urls')),
)

if settings.DEBUG:
    urlpatterns = patterns('',
                           url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                               {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
                           url(r'', include('django.contrib.staticfiles.urls')),
    ) + urlpatterns