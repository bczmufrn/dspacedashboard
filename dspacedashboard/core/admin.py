from rest_framework.authtoken.admin import TokenAdmin

from django.contrib import admin

TokenAdmin.raw_id_fields = ['user']