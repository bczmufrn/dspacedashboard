from django.contrib import admin

from dspacedashboard.autopermission.models import AutoPermissionUser

@admin.register(AutoPermissionUser)
class DepartmentAdmin(admin.ModelAdmin):
	list_display = ('netid', 'created', 'created_at')
	search_fields = ('netid', )