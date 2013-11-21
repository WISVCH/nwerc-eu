from django import forms
from livecontest.models import Registration


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        exclude = ('password', )