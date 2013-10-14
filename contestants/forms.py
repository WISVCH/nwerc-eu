from contest import forms


class ImportForm(forms.Form):
    file = forms.FileField()
