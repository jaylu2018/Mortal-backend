from django.contrib import admin
from django.urls import re_path, path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.documentation import include_docs_urls

schema_view = get_schema_view(
    openapi.Info(
        title="Peanuts API",
        default_version="V1",
        description="Peanuts接口自动化测试平台",
        terms_of_service="http://localhost:8000",
        license=openapi.License(name="Apache-2.0 License"),
    ),
    public=True,
)
urlpatterns = [
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="swagger-ui",
    ),
    re_path(r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="redoc"),
    path("docs/", include_docs_urls(title="接口文档")),
    path("", include("system.users.urls")),
    path("", include("system.menus.urls")),
    path("", include("system.roles.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("admin/", admin.site.urls),
]
