from django.core.mail import EmailMessage
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from activities.models import Subscription


class Registration(models.Model):
    login = models.CharField(_('login'), max_length=15, unique=True)
    password = models.CharField(_('password'), blank=True, null=True, max_length=100)

    email = models.EmailField(_('email'))
    name = models.CharField(_('team name'), max_length=255, unique=True)
    members = models.TextField(_('members'), blank=True)

    @property
    def authtoken(self):
        import hashlib

        return hashlib.new('%s#%s' % (self.login, self.password)).hexdigest()

    def clean(self):
        if not self.password:
            self.password = Subscription.generate_hash()

    def __unicode__(self):
        return self.name


def livecontest_created(sender, instance, created, **kwargs):
    if not created:
        return

    from django.template.loader import render_to_string

    body = render_to_string('livecontest/mail.html', {'registration': instance})

    mail = EmailMessage(
        to=(instance.email,),
        subject='Registration Online Contest NWERC 2013',
        body=body,
        from_email='NWERC 2013 <orga@nwerc.eu>',
    )

    try:
        mail.send()
    except Exception, e:
        raise e


post_save.connect(livecontest_created, sender=Registration)