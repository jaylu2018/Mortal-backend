# 用户路由
from django.urls import path, include

from system.menus import views

# 视图集管理路由，simpleRouter
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register("menus", views.MenuViewSet)

urlpatterns = [
    # 菜单路由
    path("", include(router.urls)),
    path("menus/tree", views.MenuViewSet.as_view({"get": "tree"}), name="menu-tree"),
]
