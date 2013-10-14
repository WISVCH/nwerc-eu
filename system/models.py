from django.db import models
from django.utils.translation import ugettext_lazy as _


class Computer(models.Model):
    TYPE_CHOICES = (
        ('team', 'Team'),
        ('jury', 'Jury'),
        ('free', 'Free / scoreboard'),
        ('aj', 'Autojudge'),
        ('ajlc', 'Autojudge Live Contest'),
        ('broken', 'Broken')
    )

    nwerc_number = models.CharField(_('nwerc number'), max_length=12, unique=True)
    TUD_id = models.CharField(_('TUD id'), blank=True, null=True, max_length=12, unique=True)
    ip = models.CharField(_('ip'), blank=True, null=True, max_length=15)
    mac_address = models.CharField(_('mac address'), blank=True, null=True, max_length=17)

    computer_type = models.CharField(blank=True, max_length=6, choices=TYPE_CHOICES)

    def __unicode__(self):
        return self.nwerc_number
