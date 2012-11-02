from django import forms
from models import Subscription

class ImportForm(forms.Form):
    file = forms.FileField()
    
class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        exclude = ('person', 'key', 'mail_sent')