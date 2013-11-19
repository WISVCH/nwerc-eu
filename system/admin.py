from django.conf.urls import patterns, url
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from models import Computer, TeamPlacement
from views import PlaceUnplacedTeamsView, ExportSystemZipView


class ComputerAdmin(ImportExportModelAdmin):
    list_display = ['unique_number', 'ip', 'mac_address', 'computer_type']
    list_filter = ['computer_type', ]

    def get_urls(self):
        urls = super(ComputerAdmin, self).get_urls()
        my_urls = patterns('',
                           url(r'^export-zip/$', self.admin_site.admin_view(ExportSystemZipView.as_view()),
                               name='system-admin-export-zip'),
        )
        return my_urls + urls


class TeamPlacementAdmin(ImportExportModelAdmin):
    list_display = ['computer', 'team', 'username']

    def get_urls(self):
        urls = super(TeamPlacementAdmin, self).get_urls()
        my_urls = patterns('',
                           url(r'^place-teams/$', self.admin_site.admin_view(PlaceUnplacedTeamsView.as_view()),
                               name='teamplacement-place-teams'),
        )
        return my_urls + urls


admin.site.register(Computer, ComputerAdmin)
admin.site.register(TeamPlacement, TeamPlacementAdmin)