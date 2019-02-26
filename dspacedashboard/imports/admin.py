from django.contrib import admin

from dspacedashboard.imports.models import FileImport, Collection

admin.site.register([FileImport, Collection])