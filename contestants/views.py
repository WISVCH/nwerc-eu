from StringIO import StringIO
from datetime import datetime
import zipfile
from django.contrib import messages
from django.http import HttpResponse
from django.views.generic import ListView, FormView, TemplateView
from contestants.forms import ImportForm
from contestants.models import Team, Person, Institution, Country, TeamPerson


class TeamListView(ListView):
    model = Team

    def get_queryset(self):
        qs = super(TeamListView, self).get_queryset()
        return qs.exclude(status="C")


class ImportView(FormView):
    form_class = ImportForm
    template_name = 'contest/import.html'
    success_url = '/admin/'

    def form_valid(self, form):
        zip_file = StringIO(form.cleaned_data['file'].read())
        try:
            zf = zipfile.ZipFile(zip_file, 'r')
        except:
            return self.form_invalid(form)

        f = zf.open('Person.tab', 'r')
        keys = f.readline().split('\t')
        for line in f.readlines():
            d = dict(zip(keys, line.split('\t')))
            p = Person.objects.get_or_create(person_id=d['person Id'])[0]

            p.title = d['title']
            p.first_name = d['first name']
            p.last_name = d['last name']
            p.prefered_name = d['prefered name']
            p.certificate_name = d['certificate name']
            p.gender = d['sex'][:1]
            p.email = d['email']
            if d['Date of birth'] != '' and d['Date of birth'] != 'null':
                p.date_of_birth = datetime.strptime(d['Date of birth'], '%m/%d/%Y')
            p.shirt_size = d['shirt size']
            p.save()
        f.close()

        f = zf.open('School.tab', 'r')
        keys = f.readline().split('\t')
        for line in f.readlines():
            d = dict(zip(keys, line.split('\t')))
            i = Institution.objects.get_or_create(institution_id=d['institution-unit Id'])[0]
            i.name = d['institution-unit name']
            i.short_name = d['institution-unit short name']
            i.country = Country.objects.get_or_create(ICPC_name=d['country'])[0]
            i.save()
        f.close()

        f = zf.open('Team.tab', 'r')
        keys = f.readline().split('\t')
        for line in f.readlines():
            d = dict(zip(keys, line.split('\t')))
            t = Team.objects.get_or_create(team_id=d['team Id'])[0]
            t.name = d['team Name']
            t.institution = Institution.objects.get(institution_id=d['institution-unit Id'])
            t.status = d['team status']
            # t.created = d['date created']
            t.save()
        f.close()

        TeamPerson.objects.all().delete()
        f = zf.open('TeamPerson.tab', 'r')
        keys = f.readline().split('\t')
        for line in f.readlines():
            d = dict(zip(keys, line.split('\t')))
            tp = TeamPerson.objects.get_or_create(
                person=Person.objects.get(person_id=d['person Id']),
                team=Team.objects.get(team_id=d['team Id']),
                role=d['team role']
            )
        f.close()

        messages.success(self.request, 'Successfully imported data.')
        return super(ImportView, self).form_valid(form)


class ExportImagesView(TemplateView):
    def get(self, request, *args, **kwargs):
        object_list = Institution.objects.all()

        response = HttpResponse(mimetype='application/zip')
        response['Content-Disposition'] = 'attachment; filename=affiliations.zip'

        zipdata = StringIO()
        zipf = zipfile.ZipFile(zipdata, mode="w")
        for object in object_list:
            if object.logo:
                zipf.writestr('affiliations/%s.jpg' % object.institution_id, object.logo.read())
        zipf.close()

        response.write(zipdata.getvalue())

        return response


class ExportBadgesView(TemplateView):
    def get(self, request, *args, **kwargs):
        from django.template import loader, Context

        c = Context({'object_list': TeamPerson.objects.all()})
        t = loader.get_template('contestants/badges.txt')

        response = HttpResponse(mimetype='application/txt')
        response['Content-Disposition'] = 'attachment; filename=badges.txt'

        response.write(t.render(c).encode('utf-8'))

        return response
