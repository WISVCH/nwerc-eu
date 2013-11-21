from django.views.generic import CreateView
from livecontest.forms import RegistrationForm
from livecontest.models import Registration


class RegistrationView(CreateView):
    model = Registration

    form_class = RegistrationForm

    def get_success_url(self):
        return '/online-contest/registration/success/'
