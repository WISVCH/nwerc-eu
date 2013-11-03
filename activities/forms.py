from django import forms
from activities.models import Subscription


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        exclude = ('person', 'key', 'mail_sent')