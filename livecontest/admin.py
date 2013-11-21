from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from models import Registration


admin.site.register(Registration, ImportExportModelAdmin)
