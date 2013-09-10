from django.views.generic import ListView
from contestants.models import Team


class TeamListView(ListView):
    model = Team
