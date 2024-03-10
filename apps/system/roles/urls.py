# 用户路由
from django.urls import path, include

from system.roles import views

# 视图集管理路由，simpleRouter
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register("roles", views.RoleViewSet)

urlpatterns = [
    # 角色路由
    path("", include(router.urls)),
]
