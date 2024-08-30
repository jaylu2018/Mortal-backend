from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from utils.constant import BusinessStatusCode


class CustomModelViewSet(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        pageSize = request.query_params.get("size", None)

        queryset = self.filter_queryset(self.get_queryset())

        if pageSize is not None:
            self.pagination_class.page_size = pageSize
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return CustomResponse(
                    {
                        "list": serializer.data,
                        "total": self.paginator.page.paginator.count,
                        "pageSize": pageSize,
                        "currentPage": 1
                    },
                    status=status.HTTP_200_OK,
                    busi_status=BusinessStatusCode.OPERATION_SUCCESS,
                )

        serializer = self.get_serializer(queryset, many=True)
        return CustomResponse(data=serializer.data, status=status.HTTP_200_OK, busi_status=BusinessStatusCode.OPERATION_SUCCESS)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return CustomResponse(data=serializer.data, status=status.HTTP_201_CREATED, headers=headers, busi_status=BusinessStatusCode.OPERATION_SUCCESS)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return CustomResponse(data=serializer.data, status=status.HTTP_200_OK, busi_status=BusinessStatusCode.OPERATION_SUCCESS)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return CustomResponse(status=status.HTTP_204_NO_CONTENT, busi_status=BusinessStatusCode.OPERATION_SUCCESS)


class CustomResponse(Response):
    def __init__(self, data=None, busi_status=None, status=None, template_name=None, headers=None, exception=False, content_type=None):
        datas = {
            "success": True if status in (200, 201) else False,
            "code": busi_status,
            "data": data
        }
        super().__init__(datas, status, template_name, headers, exception, content_type)
