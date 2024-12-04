from django.contrib import admin

# Register your models here.
from dspacedashboard.accounts.models import User

admin.site.register(User)