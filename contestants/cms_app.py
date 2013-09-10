from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class TeamHook(CMSApp):
    name = _('Teams')
    urls = ['teams.urls', ]
    app_name = 'teams'


apphook_pool.register(TeamHook)