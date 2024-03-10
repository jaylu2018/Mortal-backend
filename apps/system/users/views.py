from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.generics import CreateAPIView, RetrieveAPIView

from system.roles.models import Role
from system.users.models import User
from system.users.serializers import UserRegisterSerializer, UserSerializer
from system.users.serializers import MyTokenObtainPairSerializer

from system.users.serializers import MyTokenRefreshSerializer
from utils.base_viewset import CustomModelViewSet


# 登录视图，继承自TokenObtainPairView
class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        return Response(
            {
                "code": 0,
                "message": "OK",
                "data": {
                    "accessToken": serializer.validated_data["token"],
                    "refreshToken": serializer.validated_data["refresh"],
                },
            },
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get("refresh_token")
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {
                "code": 0,
                "message": "OK",
                "data": True,
            },
            status=status.HTTP_200_OK,
        )


# Token刷新视图，继承自TokenRefreshView
class MyTokenRefreshView(TokenRefreshView):
    # 指定序列化器
    serializer_class = MyTokenRefreshSerializer


# 用户注册视图
class UserRegisterView(CreateAPIView):
    # 指定序列化器
    serializer_class = UserRegisterSerializer


# 用户视图集
class UserViewSet(CustomModelViewSet):
    # 指定序列化器
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by("-date_joined")  # 按时间倒序

    def get_queryset(self):
        queryset = super().get_queryset()
        enable = self.request.query_params.get("enable", None)
        username = self.request.query_params.get("username", None)
        gender = self.request.query_params.get("gender", None)
        if enable is not None:
            queryset = queryset.filter(enable=enable)
        if gender is not None:
            queryset = queryset.filter(gender=gender)
        if username is not None:
            queryset = queryset.filter(username__icontains=username)
        return queryset

    def create(self, request, *args, **kwargs):
        role_ids = request.data.get("roleIds", [])
        roles = Role.objects.filter(id__in=role_ids)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.roles.set(roles)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"code": 0, "message": "OK", "data": serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class UserDetailView(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        return User.objects.first()

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {
                "code": 0,
                "message": "OK",
                "data": {
                    "id": 1,
                    "username": "admin",
                    "enable": True,
                    "profile": {
                        "id": 1,
                        "nickName": "Admin",
                        "avatar": "https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif?imageView2/1/w/80/h/80",
                        "userId": 1,
                    },
                    "currentRole": {"id": 1, "code": "SUPER_ADMIN", "name": "超级管理员", "enable": True},
                },
                "originUrl": "/user/detail",
            },
            status=status.HTTP_200_OK,
        )
