from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class ContestantsHook(CMSApp):
    name = _('Contestants')
    urls = ['contestants.urls', ]
    app_name = 'contestants'


apphook_pool.register(ContestantsHook)