from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class ActivityHook(CMSApp):
    name = _('Activities')
    urls = ['activities.urls', ]
    app_name = 'activities'


apphook_pool.register(ActivityHook)