from datetime import datetime
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from contestants.models import Person


class Activity(models.Model):
    title = models.CharField(_('title'), max_length=100)
    max_participants = models.PositiveIntegerField(_('max participants'))
    description = models.TextField(_('description'))

    def __unicode__(self):
        return '%s (%d free places)' % (self.title, self.max_participants - self.subscriptions.count())

    class Meta:
        verbose_name = _('activity')
        verbose_name_plural = _('activities')
        ordering = ['title', ]


class Subscription(models.Model):
    person = models.OneToOneField(Person)
    key = models.CharField(_('key'), max_length=12, unique=True)
    activity = models.ForeignKey(Activity, blank=True, null=True, related_name='subscriptions')
    hotel = models.CharField(_('hotel'), max_length=100, blank=True, null=True)
    special_needs = models.TextField(_('special needs and dietary restrictions'), blank=True, null=True)
    mail_sent = models.DateTimeField(_('mail sent'), blank=True, null=True)

    def get_absolute_url(self):
        return reverse('activities:subscribe', args=(self.person_id, self.key))

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.activity and self.activity.subscriptions.all().count() >= self.activity.max_participants:
            try:
                subscription = self.__class__.objects.get(pk=self.pk)
                if subscription.activity == self.activity:
                    return
            except:
                pass
            raise ValidationError('The activity you chose is full.')

    def send_mail(self, force=False):
        if not force and self.mail_sent:
            return

        from django.template.loader import render_to_string

        body = render_to_string('activities/contestant_mail.html', {'subscription': self})

        mail = EmailMessage(
            to=(self.person.email,),
            subject='Welcome to NWERC 2013',
            body=body,
            from_email='NWERC 2013 <orga@nwerc.eu>',
        )

        try:
            mail.send()
            self.mail_sent = datetime.now()
            self.save()
        except Exception, e:
            raise e

    @staticmethod
    def generate_hash():
        import string
        import random

        chars = string.ascii_letters + string.digits
        return ''.join([random.choice(chars) for x in range(12)])