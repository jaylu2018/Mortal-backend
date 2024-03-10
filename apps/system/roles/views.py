from django.contrib.auth.models import Permission
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from system.roles.models import Role
from system.roles.serializers import RoleSerializer
from utils.base_viewset import CustomModelViewSet


class RoleViewSet(CustomModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        enable = self.request.query_params.get("enable", None)
        name = self.request.query_params.get("name", None)
        if enable is not None:
            queryset = queryset.filter(enable=enable)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        return queryset

    def create(self, request, *args, **kwargs):
        data = request.data
        permission_ids = data.get("permissionIds", None)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        role = serializer.save()

        permissions = Permission.objects.filter(id__in=permission_ids)
        role.permissions.set(permissions)

        return Response(
            {"code": 0, "message": "OK", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )
