from django.contrib import messages
from django.views.generic import ListView, UpdateView
from activities.forms import SubscriptionForm

from models import Activity, Subscription


class ActivityListView(ListView):
    model = Activity


class SubscribeView(UpdateView):
    model = Subscription
    form_class = SubscriptionForm

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_object(self, queryset=None):
        from django.http import Http404

        try:
            return Subscription.objects.filter(person__person_id=self.kwargs.get('person_id'), key=self.kwargs.get('key')).get()
        except:
            raise Http404

    def form_valid(self, form):
        messages.success(self.request, 'Your subscription has been updated.')
        return super(SubscribeView, self).form_valid(form)
