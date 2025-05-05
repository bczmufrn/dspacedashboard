from rest_framework import serializers

from dspacedashboard.autopermission.models import AutoPermissionUser

class AutoPermissionUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutoPermissionUser
        fields = ['id', 'netid']