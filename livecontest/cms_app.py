from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class LivecontestHook(CMSApp):
    name = _('Live Contest')
    urls = ['livecontest.urls', ]
    app_name = 'livecontest'


apphook_pool.register(LivecontestHook)