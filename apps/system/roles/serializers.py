from django.contrib.auth.models import Permission
from rest_framework import serializers
from .models import Role


class RoleSerializer(serializers.ModelSerializer):
    permissionIds = serializers.PrimaryKeyRelatedField(
        source="permissions", many=True, queryset=Permission.objects.all()
    )

    class Meta:
        model = Role
        fields = ("id", "name", "code", "order", "enable", "description", "permissionIds")
