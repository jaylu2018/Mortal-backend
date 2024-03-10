from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class CustomModelViewSet(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        pageSize = request.query_params.get("pageSize", None)

        queryset = self.filter_queryset(self.get_queryset())

        if pageSize is not None:
            self.pagination_class.page_size = pageSize
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return Response(
                    {
                        "code": 0,
                        "message": "OK",
                        "data": {
                            "pageData": serializer.data,
                            "total": self.paginator.page.paginator.count,
                        },
                        "originUrl": request.build_absolute_uri(),
                    },
                    status=status.HTTP_200_OK,
                )

        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {"code": 0, "message": "OK", "data": serializer.data},
            status=status.HTTP_200_OK,
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"code": 0, "message": "OK", "data": serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers,
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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {
                "code": 0,
                "message": "OK",
                "data": "OK",
            },
            status=status.HTTP_200_OK,
        )
