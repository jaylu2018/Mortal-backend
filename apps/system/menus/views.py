from rest_framework import viewsets, status
from rest_framework.response import Response

from system.menus.models import Menu
from system.menus.serializers import MenuSerializer


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def create(self, request, *args, **kwargs):
        children_data = request.data.pop("children", None)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        menu = serializer.save()
        if children_data is not None:
            for child_data in children_data:
                Menu.objects.create(parent=menu, **child_data)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"code": 0, "message": "OK", "data": serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def list(self, request, *args, **kwargs):
        queryset = Menu.objects.filter(parentId=None)
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {"code": 0, "message": "OK", "data": serializer.data},
            status=status.HTTP_200_OK,
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(
            {"code": 0, "message": "OK", "data": serializer.data},
            status=status.HTTP_200_OK,
        )

    def tree(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
