# 用户路由
from django.urls import path, include

from system.users import views

# 视图集管理路由，simpleRouter
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register("users", views.UserViewSet)

urlpatterns = [
    # 用户登录
    path("auth/login", views.LoginView.as_view(), name="login"),
    # 用户退出
    path("auth/logout", views.LogoutView.as_view(), name="logout"),
    # 刷新token
    path("users/token/refresh", views.MyTokenRefreshView.as_view(), name="refresh"),
    # 用户注册
    path("users/register", views.UserRegisterView.as_view(), name="register"),
    # 用户路由
    path("", include(router.urls)),
    # 用户详情
    path("users/details", views.UserDetailView.as_view(), name="user-detail"),
]
