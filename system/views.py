from django.db.models import Q
from django.views.generic import TemplateView
from contestants.models import Team
from system.models import TeamPlacement, Computer


class PlaceUnplacedTeamsView(TemplateView):
    template_name = "system/place_unplaced_teams.html"

    def get(self, request, *args, **kwargs):
        teamplacements = zip(*TeamPlacement.objects.all().values_list('computer', 'team'))

        if(len(teamplacements) == 0):
            teamplacements = [[],[]]

        available_computers = list(Computer.objects \
            .filter(Q(computer_type="free") | Q(computer_type="team")) \
            .exclude(pk__in=teamplacements[0]) \
            .order_by('?'))

        teams = Team.objects \
            .filter(status="A") \
            .exclude(pk__in=teamplacements[1])

        teams_placed = []
        teams_unplaced = []

        for team in teams:

            if len(available_computers) > 0:
                computer = available_computers.pop()
                team.move(computer)
                teams_placed.append(team)
            else:
                teams_unplaced.append(team)

        return super(PlaceUnplacedTeamsView, self).get(request, teams_placed=teams_placed, teams_unplaced=teams_unplaced)
