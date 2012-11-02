from django.http import HttpResponseRedirect
from django.views.generic import FormView, ListView, TemplateView, UpdateView
from cStringIO import StringIO

from forms import ImportForm, SubscriptionForm
from models import Person, Team, Institution, Country, TeamPerson, Event, Subscription
import zipfile
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages

class EventView(ListView):
    model = Event

class EventSubscriptionView(ListView):
    model = Event
    template_name = 'contest/event_list_subscriptions.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EventSubscriptionView, self).dispatch(*args, **kwargs)
        
class SubscribeView(UpdateView):
    model      = Subscription
    form_class = SubscriptionForm
    
    def get_success_url(self):
        return self.object.get_absolute_url()
    
    def get_object(self, queryset=None):
        from django.http import Http404
        try:
            return Subscription.objects.filter(person=self.kwargs.get('person_id'), key=self.kwargs.get('key')).get()
        except:
            raise Http404
        
    def form_valid(self, form):
        messages.success(self.request, 'Your subscription has been updated.')
        return super(SubscribeView, self).form_valid(form)
    
class TeamView(ListView):
    model = Team

class ImportView(FormView):
    form_class = ImportForm
    template_name = 'contest/import.html'
    success_url = '/admin/'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/admin/')

        return super(ImportView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        zip_file = StringIO(form.cleaned_data['file'].read())
        try:
            zf = zipfile.ZipFile(zip_file, 'r')
        except:    
            return self.form_invalid(form)

        f = zf.open('Person.tab','r')
        keys = f.readline().split('\t')
        for line in f.readlines():
          d = dict(zip(keys, line.split('\t')))
          p = Person.objects.get_or_create(person_id=d['person Id'])[0]
          
          p.title = d['title']
          p.first_name = d['first name']
          p.last_name = d['last name']
          p.prefered_name = d['prefered name']
          p.certificate_name = d['certificate name']
          p.gender = d['gender'][:1]
          p.email = d['email']
          if d['Date of birth'] != '' and d['Date of birth'] != 'null':
            p.date_of_birth = datetime.strptime(d['Date of birth'],'%m/%d/%Y')
          p.shirt_size = d['shirt size']
          p.save()
        f.close()

        f = zf.open('School.tab','r')
        keys = f.readline().split('\t')
        for line in f.readlines():
          d = dict(zip(keys, line.split('\t')))
          i = Institution.objects.get_or_create(institution_id=d['institution Id'])[0]
          i.name = d['institution Name']
          i.short_name = d['institution short name'] 
          i.country = Country.objects.get_or_create(ICPC_name=d['country'])[0]
          i.save()
        f.close()

        f = zf.open('Team.tab','r')
        keys = f.readline().split('\t')
        for line in f.readlines():
          d = dict(zip(keys, line.split('\t')))
          t = Team.objects.get_or_create(team_id=d['team Id'])[0]
          t.name = d['team Name']
          t.institution = Institution.objects.get(institution_id=d['institution Id'])
          t.status = d['team status']
          # t.created = d['date created']
          t.save()
        f.close()
        
        TeamPerson.objects.all().delete()
        f = zf.open('TeamPerson.tab','r')
        keys = f.readline().split('\t')
        for line in f.readlines():
          d = dict(zip(keys, line.split('\t')))
          tp = TeamPerson.objects.get_or_create(
            person = Person.objects.get(person_id=d['person Id']),
            team = Team.objects.get(team_id=d['team Id']),
            role = d['team role']
          )
        f.close()

        messages.success(self.request, 'Succesfully imported data.')
        return super(ImportView, self).form_valid(form)
        
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ImportView, self).dispatch(*args, **kwargs)
            
class SendMailsView(TemplateView):
    def get(self, request, *args, **kwargs):
        for person in Person.objects.all():
            person.get_or_create_subscription()
        
        messages.success(request, 'Mails are sent (to persons not sent yet (and team approved)).')
        return HttpResponseRedirect('/admin/')
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SendMailsView, self).dispatch(*args, **kwargs)
