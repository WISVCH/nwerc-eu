from django.contrib import admin
from cms.admin.placeholderadmin import PlaceholderAdmin

from models import Person, Team, TeamPerson, Institution, Country, Event, Subscription, Computer, TeamPlacement, LiveContestRegistration


class SubscriptionInline(admin.TabularInline):
    model = Subscription
    extra = 0


class TeamPersonInline(admin.TabularInline):
    model = TeamPerson
    extra = 0


class PersonAdmin(admin.ModelAdmin):
    search_fields = ('first_name', 'last_name', 'email')
    list_display = ('first_name', 'last_name', 'email', 'date_of_birth', 'gender', 'shirt_size')
    list_filter = ('gender', 'shirt_size')
    inlines = (TeamPersonInline, SubscriptionInline)


class TeamAdmin(admin.ModelAdmin):
    inlines = (TeamPersonInline,)


class CountryAdmin(admin.ModelAdmin):
    list_display = ('ICPC_name', 'name', 'iso_3166_1')
    list_editable = ('name', 'iso_3166_1')


class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'logo')
    list_editable = ('short_name', 'logo',)


admin.site.register(Person, PersonAdmin)
admin.site.register(Team, TeamAdmin)
# admin.site.register(TeamPerson)
admin.site.register(Institution, InstitutionAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Event, PlaceholderAdmin)
admin.site.register(Computer)
admin.site.register(TeamPlacement)
admin.site.register(LiveContestRegistration)