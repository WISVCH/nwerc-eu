from django import forms
from models import Subscription, LiveContestRegistration


class ImportForm(forms.Form):
    file = forms.FileField()


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        exclude = ('person', 'key', 'mail_sent')


class LiveContestRegistrationForm(forms.ModelForm):
    class Meta:
        model = LiveContestRegistration
        exclude = ('password')