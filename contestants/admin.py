from django.conf.urls import patterns, url
from django.contrib import admin
from contestants.models import Person, Team, Country, Institution, TeamPerson
from contestants.views import ImportView


class TeamPersonInline(admin.TabularInline):
    model = TeamPerson
    extra = 0


class PersonAdmin(admin.ModelAdmin):
    search_fields = ('first_name', 'last_name', 'email')
    list_display = ('first_name', 'last_name', 'email', 'date_of_birth', 'gender', 'shirt_size')
    list_filter = ('gender', 'shirt_size')
    inlines = (TeamPersonInline,)

    def get_urls(self):
        urls = super(PersonAdmin, self).get_urls()
        my_urls = patterns('',
                           url(r'^import/$', self.admin_site.admin_view(ImportView.as_view()),
                               name='contestants-admin-import'),
        )
        return my_urls + urls


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
admin.site.register(Country, CountryAdmin)
admin.site.register(Institution, InstitutionAdmin)
