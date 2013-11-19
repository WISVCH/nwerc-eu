from cStringIO import StringIO
import zipfile
from datetime import datetime
from django.db.models import Q
from django.http import HttpResponse
from django.views.generic import TemplateView
from contestants.models import Team
from system.models import TeamPlacement, Computer


class PlaceUnplacedTeamsView(TemplateView):
    template_name = "system/place_unplaced_teams.html"

    def get(self, request, *args, **kwargs):
        teamplacements = zip(*TeamPlacement.objects.all().values_list('computer', 'team'))

        if (len(teamplacements) == 0):
            teamplacements = [[], []]

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

        return super(PlaceUnplacedTeamsView, self).get(request, teams_placed=teams_placed,
                                                       teams_unplaced=teams_unplaced)


class ExportSystemZipView(TemplateView):
    def get(self, request, *args, **kwargs):
        from django.template import loader, Context

        response = HttpResponse(mimetype='application/zip')
        response['Content-Disposition'] = 'attachment; filename=export.zip'

        zipdata = StringIO()
        zipf = zipfile.ZipFile(zipdata, mode="w")

        c = Context({'object_list': Computer.objects.exclude(computer_type='broken'), 'date': datetime.now()})

        #t = loader.get_template('system/generation/hosts.main-server')
        #zipf.writestr('affiliations.sql', Export.get_affiliations_sql().encode('utf-8'))
        #zipf.writestr('teams.sql', Export.get_teams_sql().encode('utf-8'))
        #zipf.writestr('livecontest/teams.sql', Export.get_live_contest_teams().encode('utf-8'))
        #zipf.writestr('livecontest/affiliations.sql', Export.get_live_contest_affiliations().encode('utf-8'))
        t = loader.get_template('system/generation/hosts.main-server')
        zipf.writestr('hosts', t.render(c))
        t = loader.get_template('system/generation/genders')
        zipf.writestr('genders', t.render(c).encode('utf-8'))
        t = loader.get_template('system/generation/dhcpd.conf')
        zipf.writestr('dhcpd.conf', t.render(c).encode('utf-8'))
        t = loader.get_template('system/generation/HOST_MAC_TABLE')
        zipf.writestr('HOST_MAC_TABLE', t.render(c).encode('utf-8'))
        t = loader.get_template('system/generation/IP_HOST_TABLE')
        zipf.writestr('IP_HOST_TABLE', t.render(c).encode('utf-8'))

        #for object in Institution.objects.all():
        #    if object.logo:
        #        zipf.writestr('affiliations/%s.jpg' % object.institution_id, object.logo_thumb.read())

        zipf.close()
        response.write(zipdata.getvalue())
        return response
