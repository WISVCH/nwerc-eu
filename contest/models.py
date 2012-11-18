from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save

from cms.models.fields import PlaceholderField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
from datetime import datetime


class Country(models.Model):
    ICPC_name  = models.CharField(_('ICPC name'), max_length=3)
    name       = models.CharField(_('name'), max_length=55, blank=True, null=True)
    iso_3166_1 = models.CharField(_('ISO 3166-1 Alpha 2 code'), max_length=2, blank=True, null=True)

    def get_flag_url(self):
        return 'img/flags/%s.png' % self.iso_3166_1

    def __unicode__(self):
        if self.name:
            return self.name
        return self.ICPC_name
        
    class Meta:
        verbose_name = _('country')
        verbose_name_plural = _('countries')


class Institution(models.Model):
    institution_id = models.IntegerField(_('institution_id'), primary_key=True)
    name           = models.CharField(_('name'), max_length=255, blank=True, null=True)
    short_name     = models.CharField(_('short name'), max_length=55, blank=True, null=True)
    country        = models.ForeignKey(Country, blank=True, null=True)
    logo           = models.ImageField(_('logo'), upload_to='institutions', blank=True, null=True)

    logo_thumb = ImageSpecField([ResizeToFit(width=24,height=24),], image_field='logo')

    def __unicode__(self):
        return self.name


class Reminder(models.Model):
    subscription = models.OneToOneField('Subscription')
    mail_sent = models.DateTimeField(_('mail sent'), blank=True, null=True)
    
    def send_mail(self, force=False):
        if not force and self.mail_sent:
            return

        from django.template.loader import render_to_string
        body = render_to_string('contest/reminder_mail.html', {'subscription':self.subscription})
        
        mail = EmailMessage(
            to         = (self.subscription.person.email,),
            subject    = 'NWERC Activity reminder',
            body       = body,
            from_email = 'NWERC 2012 <orga@nwerc.eu>',
        )
        
        try:
            mail.send()
            self.mail_sent = datetime.now()
            self.save()
        except Exception, e:
            raise e


class Subscription(models.Model):
    person    = models.OneToOneField('Person')
    key       = models.CharField(_('key'), max_length=12, unique=True)
    event     = models.ForeignKey('Event', blank=True, null=True, related_name='subscriptions')
    hotel     = models.CharField(_('hotel'), max_length=100, blank=True, null=True)
    mail_sent = models.DateTimeField(_('mail sent'), blank=True, null=True)

    def get_absolute_url(self):
        return reverse('contest:subscribe', args=(self.person_id, self.key))

    def clean(self):
        from django.core.exceptions import ValidationError
        
        if self.event and self.event.subscriptions.all().count() >= self.event.max_participants:
            try:
                subscription = self.__class__.objects.get(pk=self.pk)
                print subscription
                if subscription.event == self.event:
                    return
            except:
                pass
            raise ValidationError('The activity you chose is full.')

    def send_mail(self, force=False):
        if not force and self.mail_sent:
            return

        from django.template.loader import render_to_string
        body = render_to_string('contest/contestant_mail.html', {'subscription':self})
        
        mail = EmailMessage(
            to         = (self.person.email,),
            subject    = 'Welcome to NWERC 2012',
            body       = body,
            from_email = 'NWERC 2012 <orga@nwerc.eu>',
        )
        
        try:
            mail.send()
            self.mail_sent = datetime.now()
            self.save()
        except Exception, e:
            raise e

    def get_or_create_reminder(self):
        if not self.mail_sent or self.event:
            print "no reminder"
            return None
        
        try:
            return Reminder.objects.filter(subscription=self).get()
        except:
            reminder = Reminder(subscription=self)
            reminder.save()
            reminder.send_mail()
            return reminder

    @staticmethod
    def generate_hash():
        import string
        import random

        chars = string.ascii_letters + string.digits
        return ''.join([random.choice(chars) for x in range(12)])

    
class TeamPerson(models.Model):
    ROLE_CHOICES = (
        ('CONTESTANT', 'Contestant'),
        ('COACH', 'Coach'),
        ('RESERVE', 'Reserve'),
        ('ATTENDEE', 'Attendee'),
    )

    person = models.ForeignKey('Person')
    team   = models.ForeignKey('Team')
    role   = models.CharField(_('role'), max_length=15, choices=ROLE_CHOICES)


class Person(models.Model):
    person_id        = models.IntegerField(_('person id'), primary_key=True)
    title            = models.CharField(_('title'), max_length=20, blank=True, null=True)
    first_name       = models.CharField(_('first name'), max_length=50, blank=True, null=True)
    last_name        = models.CharField(_('last name'), max_length=50, blank=True, null=True)
    prefered_name    = models.CharField(_('prefered name'), max_length=120, blank=True, null=True)
    certificate_name = models.CharField(_('certificate name'), max_length=120, blank=True, null=True)
    email            = models.EmailField(_('email'), blank=True, null=True)
    date_of_birth    = models.DateField(_('Date of birth'), blank=True, null=True)
    gender           = models.CharField(_('gender'), max_length=1, choices=(('M', 'MALE'), ('F', 'FEMALE'), ), blank=True, null=True)
    shirt_size       = models.CharField(_('shirt size'), max_length=10, blank=True, null=True)

    @property
    def is_coach(self):
        try:
            TeamPerson.objects.filter(person=self, role='COACH').get()
            return True
        except:
            return False

    def __unicode__(self):
        return self.prefered_name
        
    def get_or_create_subscription(self):
        if self.teams.filter(status='A').count() < 1:
            return None
        try:
            subscription = Subscription.objects.filter(person=self).get()
        except:
            subscription = Subscription(person=self)
            subscription.key = Subscription.generate_hash()
            subscription.save()
            subscription.send_mail()
        
        return subscription


class Team(models.Model):
    class Meta:
        ordering = ('name', )

    team_id     = models.IntegerField(_('team id'), primary_key=True)
    name        = models.CharField(_('name'), max_length=255, blank=True, null=True)
    institution = models.ForeignKey(Institution, blank=True, null=True)
    status      = models.CharField(_('status'), max_length=10, blank=True, null=True)
    created     = models.DateField(_('created'), blank=True, null=True)

    members = models.ManyToManyField(Person, through='TeamPerson', related_name='teams', blank=True, null=True)

    def __unicode__(self):
        return self.name


class Event(models.Model):
    title            = models.CharField(_('title'), max_length=100)
    max_participants = models.PositiveIntegerField(_('max participants'))
    description      = PlaceholderField('description')

    def __unicode__(self):
        return '%s (%d free places)' % (self.title, self.max_participants - self.subscriptions.count())

    class Meta:
        verbose_name = _('activity')
        verbose_name_plural = _('activities')
        ordering = ['title',]


class Computer(models.Model):
    TYPE_CHOICES = (
        ('team', 'Team'),
        ('jury', 'Jury'),
        ('free', 'Free / scoreboard'),
        ('aj', 'Autojudge'),
        ('broken', 'Broken')
    )
    
    nwerc_number = models.CharField(_('nwerc number'), max_length=12, unique=True)
    TUD_number   = models.CharField(_('TUD number'), blank=True, null=True, max_length=12, unique=True)
    ip           = models.CharField(_('ip'), blank=True, null=True, max_length=15)
    mac_address  = models.CharField(_('mac address'), blank=True, null=True, max_length=17)
    
    computer_type = models.CharField(blank=True, max_length=6, choices=TYPE_CHOICES)

    def __unicode__(self):
        return self.nwerc_number


class TeamPlacement(models.Model):
    team     = models.ForeignKey(Team)
    computer = models.ForeignKey(Computer)
    username = models.CharField(_('username'), blank=True, null=True, max_length=15)

    def __unicode__(self):
        return "%s %s" % (self.computer.nwerc_number, self.team.name)


class CountriesAlpha3(models.Model):
    code = models.CharField(_('code'), max_length=3, primary_key=True)
    name = models.CharField(_('name'), max_length=255)
    
    def __unicode__(self):
        return self.name


class LiveContestRegistration(models.Model):
    login = models.CharField(_('login'), max_length=15, unique=True)
    password = models.CharField(_('password'), blank=True, null=True, max_length=100)

    email = models.EmailField(_('email'))
    name = models.CharField(_('team name'), max_length=255, unique=True)
    members = models.TextField(_('members'), blank=True)
    country = models.ForeignKey(CountriesAlpha3)

    def clean(self):
        if not self.password:
            self.password = Subscription.generate_hash()
            
    def __unicode__(self):
        return self.name
    

def livecontest_created(sender, instance, created, **kwargs):
    if not created:
        return
    
    from django.template.loader import render_to_string
    body = render_to_string('contest/livecontestregistration_mail.html', {'registration':instance})
        
    mail = EmailMessage(
        to         = (instance.email,),
        subject    = 'Registration Online Contest NWERC 2012',
        body       = body,
        from_email = 'NWERC 2012 <orga@nwerc.eu>',
    )
        
    try:
        mail.send()
    except Exception, e:
        raise e
    
post_save.connect(livecontest_created, sender=LiveContestRegistration)
