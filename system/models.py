from django.db import models
from django.utils.translation import ugettext_lazy as _
from contestants.models import Team


class Computer(models.Model):
    TYPE_CHOICES = (
        ('team', 'Team'),
        ('jury', 'Jury'),
        ('free', 'Free'),
        ('aj', 'Autojudge'),
        ('ajlc', 'Autojudge Live Contest'),
        ('broken', 'Broken'),
        ('score', 'Scoreboard'),
        ('reserv', 'Reserve')
    )

    unique_number = models.CharField(_('nwerc number'), max_length=12, unique=True)
    TUD_id = models.CharField(_('TUD id'), blank=True, null=    True, max_length=12)
    ip = models.CharField(_('ip'), blank=True, null=True, max_length=15)
    mac_address = models.CharField(_('mac address'), blank=True, null=True, max_length=17)
    hostname = models.CharField(_('hostname'), blank=True, null=True, max_length=55)

    computer_type = models.CharField(blank=True, max_length=6, choices=TYPE_CHOICES)

    def __unicode__(self):
        return self.unique_number

    @property
    def is_free(self):
        return self.computer_type == 'free' or (self.computer_type == 'team' and not self.teamplacement_set.exists())


class TeamPlacement(models.Model):
    computer = models.ForeignKey(Computer, verbose_name=_('Team placement'), related_name='team_placement')
    team = models.ForeignKey(Team, verbose_name=_('Team'), related_name='team_placement')
    username = models.CharField(_('username'), max_length=15)

    def move(self, computer):
        if computer.computer_type == 'team':
            self.computer = computer
            self.save()
