from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models.fields import PlaceholderField


class Activity(models.Model):
    title            = models.CharField(_('title'), max_length=100)
    max_participants = models.PositiveIntegerField(_('max participants'))
    description      = models.TextField(_('description'))

    def __unicode__(self):
        return '%s (%d free places)' % (self.title, self.max_participants)

    class Meta:
        verbose_name = _('activity')
        verbose_name_plural = _('activities')
        ordering = ['title',]