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
from utils.base_viewset import CustomModelViewSet, CustomResponse
from utils.constant import BusinessStatusCode


# 登录视图，继承自TokenObtainPairView
class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        print(serializer.validated_data)
        return CustomResponse(
            {
                "accessToken": serializer.validated_data["token"],
                "refreshToken": serializer.validated_data["refresh"],
                "username": serializer.validated_data["username"],
            },
            status=status.HTTP_200_OK,
            busi_status=BusinessStatusCode.OPERATION_SUCCESS,
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
                "success": True,
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
        return CustomResponse(data=serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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
                "success": True,
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


# 获取异步路由
class AsyncRoutesView(APIView):
    # 取消鉴权
    permission_classes = [AllowAny]

    def get(self, request):
        return Response(
            {
                "data": [
                    {
                        "pk": "050f7e13-cf60-4c1d-b791-3ab6a97254f6",
                        "name": "system",
                        "rank": 1,
                        "path": "/system",
                        "component": "",
                        "meta": {
                            "title": "menus.hssysManagement",
                            "icon": "ep:setting",
                            "showParent": False,
                            "showLink": True,
                            "extraIcon": "",
                            "keepAlive": False,
                            "frameSrc": "",
                            "frameLoading": False,
                            "transition": {
                                "enterTransition": "",
                                "leaveTransition": ""
                            },
                            "hiddenTag": False,
                            "dynamicLevel": 0,
                            "auths": []
                        },
                        "parent": None,
                        "menu_type": 0,
                        "is_active": True,
                        "menu_type_display": "目录",
                        "model": [],
                        "field": [],
                        "children": [
                            {
                                "pk": "4f9726d3-3796-4602-a716-1337ee2a168e",
                                "name": "SystemUser",
                                "rank": 2,
                                "path": "/system/user/index",
                                "component": "system/user/index",
                                "meta": {
                                    "title": "menus.hsUser",
                                    "icon": "ep:user",
                                    "showParent": False,
                                    "showLink": True,
                                    "extraIcon": "",
                                    "keepAlive": False,
                                    "frameSrc": "",
                                    "frameLoading": False,
                                    "transition": {
                                        "enterTransition": "",
                                        "leaveTransition": ""
                                    },
                                    "hiddenTag": False,
                                    "dynamicLevel": 0,
                                    "auths": [
                                        "create:systemUser",
                                        "delete:systemUser",
                                        "update:systemUser",
                                        "list:systemUser",
                                        "manyDelete:systemUser",
                                        "upload:systemAvatar",
                                        "update:systemUserPwd"
                                    ]
                                },
                                "parent": "050f7e13-cf60-4c1d-b791-3ab6a97254f6",
                                "menu_type": 1,
                                "is_active": True,
                                "menu_type_display": "菜单",
                                "model": [],
                                "field": []
                            },
                            {
                                "pk": "8c6f0f01-a29e-4d72-96a8-abf67a4ede65",
                                "name": "SystemDept",
                                "rank": 11,
                                "path": "/system/dept/index",
                                "component": "system/dept/index",
                                "meta": {
                                    "title": "menus.hsDept",
                                    "icon": "ri:group-line",
                                    "showParent": False,
                                    "showLink": True,
                                    "extraIcon": "",
                                    "keepAlive": False,
                                    "frameSrc": "",
                                    "frameLoading": False,
                                    "transition": {
                                        "enterTransition": "",
                                        "leaveTransition": ""
                                    },
                                    "hiddenTag": False,
                                    "dynamicLevel": 0,
                                    "auths": [
                                        "list:systemDept",
                                        "create:systemDept",
                                        "delete:systemDept",
                                        "update:systemDept",
                                        "manyDelete:systemDept",
                                        "empower:systemDeptRole"
                                    ]
                                },
                                "parent": "050f7e13-cf60-4c1d-b791-3ab6a97254f6",
                                "menu_type": 1,
                                "is_active": True,
                                "menu_type_display": "菜单",
                                "model": [],
                                "field": []
                            },
                            {
                                "pk": "4f569df2-6149-462f-ad50-27f24370f5e2",
                                "name": "SystemMenu",
                                "rank": 18,
                                "path": "/system/menu/index",
                                "component": "system/menu/index",
                                "meta": {
                                    "title": "menus.hsMenu",
                                    "icon": "ep:menu",
                                    "showParent": False,
                                    "showLink": True,
                                    "extraIcon": "",
                                    "keepAlive": False,
                                    "frameSrc": "",
                                    "frameLoading": False,
                                    "transition": {
                                        "enterTransition": "",
                                        "leaveTransition": ""
                                    },
                                    "hiddenTag": False,
                                    "dynamicLevel": 0,
                                    "auths": [
                                        "list:systemMenu",
                                        "list:systemMenuPermission"
                                    ]
                                },
                                "parent": "050f7e13-cf60-4c1d-b791-3ab6a97254f6",
                                "menu_type": 1,
                                "is_active": True,
                                "menu_type_display": "菜单",
                                "model": [],
                                "field": []
                            },
                            {
                                "pk": "1e11bae7-8002-4e92-a215-9eb4d3e8876c",
                                "name": "config",
                                "rank": 26,
                                "path": "/system/configs",
                                "component": "",
                                "meta": {
                                    "title": "menus.hsConfig",
                                    "icon": "ep:connection",
                                    "showParent": False,
                                    "showLink": True,
                                    "extraIcon": "",
                                    "keepAlive": False,
                                    "frameSrc": "",
                                    "frameLoading": False,
                                    "transition": {
                                        "enterTransition": "",
                                        "leaveTransition": ""
                                    },
                                    "hiddenTag": False,
                                    "dynamicLevel": 0,
                                    "auths": []
                                },
                                "parent": "050f7e13-cf60-4c1d-b791-3ab6a97254f6",
                                "menu_type": 0,
                                "is_active": True,
                                "menu_type_display": "目录",
                                "model": [],
                                "field": [],
                                "children": [
                                    {
                                        "pk": "6e914168-2d0e-4a35-98c1-1543cb2c2fb7",
                                        "name": "SystemConfig",
                                        "rank": 27,
                                        "path": "/system/config/system/index",
                                        "component": "system/config/system/index",
                                        "meta": {
                                            "title": "menus.hsSystemConfig",
                                            "icon": "ep:data-analysis",
                                            "showParent": False,
                                            "showLink": True,
                                            "extraIcon": "",
                                            "keepAlive": False,
                                            "frameSrc": "",
                                            "frameLoading": False,
                                            "transition": {
                                                "enterTransition": "",
                                                "leaveTransition": ""
                                            },
                                            "hiddenTag": False,
                                            "dynamicLevel": 0,
                                            "auths": [
                                                "list:systemSystemConfig"
                                            ]
                                        },
                                        "parent": "1e11bae7-8002-4e92-a215-9eb4d3e8876c",
                                        "menu_type": 1,
                                        "is_active": True,
                                        "menu_type_display": "菜单",
                                        "model": [],
                                        "field": []
                                    }
                                ],
                                "count": 1
                            },
                            {
                                "pk": "96772790-53e4-4113-b1d1-10998fe2f616",
                                "name": "permissions",
                                "rank": 41,
                                "path": "/system/permissions",
                                "component": "",
                                "meta": {
                                    "title": "menus.hsPermission",
                                    "icon": "ep:lock",
                                    "showParent": False,
                                    "showLink": True,
                                    "extraIcon": "",
                                    "keepAlive": False,
                                    "frameSrc": "",
                                    "frameLoading": False,
                                    "transition": {
                                        "enterTransition": "",
                                        "leaveTransition": ""
                                    },
                                    "hiddenTag": False,
                                    "dynamicLevel": 0,
                                    "auths": []
                                },
                                "parent": "050f7e13-cf60-4c1d-b791-3ab6a97254f6",
                                "menu_type": 0,
                                "is_active": True,
                                "menu_type_display": "目录",
                                "model": [],
                                "field": [],
                                "children": [
                                    {
                                        "pk": "b5f6aa93-62dd-433f-9759-2f542baae423",
                                        "name": "SystemRole",
                                        "rank": 42,
                                        "path": "/system/role/index",
                                        "component": "system/role/index",
                                        "meta": {
                                            "title": "menus.hsRole",
                                            "icon": "ep:scale-to-original",
                                            "showParent": False,
                                            "showLink": True,
                                            "extraIcon": "",
                                            "keepAlive": False,
                                            "frameSrc": "",
                                            "frameLoading": False,
                                            "transition": {
                                                "enterTransition": "",
                                                "leaveTransition": ""
                                            },
                                            "hiddenTag": False,
                                            "dynamicLevel": 0,
                                            "auths": [
                                                "create:systemRole",
                                                "delete:systemRole",
                                                "update:systemRole",
                                                "list:systemRole",
                                                "manyDelete:systemRole",
                                                "detail:systemRole"
                                            ]
                                        },
                                        "parent": "96772790-53e4-4113-b1d1-10998fe2f616",
                                        "menu_type": 1,
                                        "is_active": True,
                                        "menu_type_display": "菜单",
                                        "model": [],
                                        "field": []
                                    },
                                    {
                                        "pk": "0678cc57-f292-4287-887b-ffade834dde1",
                                        "name": "SystemDataPermission",
                                        "rank": 49,
                                        "path": "/system/permission/index",
                                        "component": "system/permission/index",
                                        "meta": {
                                            "title": "menus.hsDataPermission",
                                            "icon": "ep:refrigerator",
                                            "showParent": False,
                                            "showLink": True,
                                            "extraIcon": "",
                                            "keepAlive": False,
                                            "frameSrc": "",
                                            "frameLoading": False,
                                            "transition": {
                                                "enterTransition": "",
                                                "leaveTransition": ""
                                            },
                                            "hiddenTag": False,
                                            "dynamicLevel": 0,
                                            "auths": [
                                                "list:systemDataPermission",
                                                "create:systemDataPermission",
                                                "delete:systemDataPermission",
                                                "update:systemDataPermission",
                                                "manyDelete:systemDataPermission"
                                            ]
                                        },
                                        "parent": "96772790-53e4-4113-b1d1-10998fe2f616",
                                        "menu_type": 1,
                                        "is_active": True,
                                        "menu_type_display": "菜单",
                                        "model": [],
                                        "field": []
                                    },
                                    {
                                        "pk": "de2bdbf8-aeaf-4171-b73e-17cc383298d2",
                                        "name": "SystemModelLabelField",
                                        "rank": 55,
                                        "path": "/system/field/index",
                                        "component": "system/field/index",
                                        "meta": {
                                            "title": "menus.hsModelField",
                                            "icon": "ep:office-building",
                                            "showParent": False,
                                            "showLink": True,
                                            "extraIcon": "",
                                            "keepAlive": False,
                                            "frameSrc": "",
                                            "frameLoading": False,
                                            "transition": {
                                                "enterTransition": "",
                                                "leaveTransition": ""
                                            },
                                            "hiddenTag": False,
                                            "dynamicLevel": 0,
                                            "auths": [
                                                "list:systemModelField",
                                                "list:systemModelFieldLookups"
                                            ]
                                        },
                                        "parent": "96772790-53e4-4113-b1d1-10998fe2f616",
                                        "menu_type": 1,
                                        "is_active": True,
                                        "menu_type_display": "菜单",
                                        "model": [],
                                        "field": []
                                    }
                                ],
                                "count": 3
                            },
                            {
                                "pk": "74defdba-9645-439a-bf36-c0545bb9cda1",
                                "name": "logs",
                                "rank": 59,
                                "path": "/system/logs",
                                "component": "",
                                "meta": {
                                    "title": "menus.hsLog",
                                    "icon": "ep:files",
                                    "showParent": False,
                                    "showLink": True,
                                    "extraIcon": "",
                                    "keepAlive": False,
                                    "frameSrc": "",
                                    "frameLoading": False,
                                    "transition": {
                                        "enterTransition": "",
                                        "leaveTransition": ""
                                    },
                                    "hiddenTag": False,
                                    "dynamicLevel": 0,
                                    "auths": []
                                },
                                "parent": "050f7e13-cf60-4c1d-b791-3ab6a97254f6",
                                "menu_type": 0,
                                "is_active": True,
                                "menu_type_display": "目录",
                                "model": [],
                                "field": [],
                                "children": [
                                    {
                                        "pk": "33662086-715b-4478-b60d-a346c8c4f66b",
                                        "name": "SystemOperationLog",
                                        "rank": 60,
                                        "path": "/system/logs/operation/index",
                                        "component": "system/logs/operation/index",
                                        "meta": {
                                            "title": "menus.hsOperationLog",
                                            "icon": "ep:document",
                                            "showParent": False,
                                            "showLink": True,
                                            "extraIcon": "",
                                            "keepAlive": False,
                                            "frameSrc": "",
                                            "frameLoading": False,
                                            "transition": {
                                                "enterTransition": "",
                                                "leaveTransition": ""
                                            },
                                            "hiddenTag": False,
                                            "dynamicLevel": 0,
                                            "auths": [
                                                "delete:systemOperationLog",
                                                "list:systemOperationLog",
                                                "manyDelete:systemOperationLog"
                                            ]
                                        },
                                        "parent": "74defdba-9645-439a-bf36-c0545bb9cda1",
                                        "menu_type": 1,
                                        "is_active": True,
                                        "menu_type_display": "菜单",
                                        "model": [],
                                        "field": []
                                    },
                                    {
                                        "pk": "45b14edf-5f9e-4ec8-bc4d-3c6f0b9c851b",
                                        "name": "SystemUserLoginLog",
                                        "rank": 64,
                                        "path": "/system/logs/login/index",
                                        "component": "system/logs/login/index",
                                        "meta": {
                                            "title": "menus.hsLoginLog",
                                            "icon": "ep:cellphone",
                                            "showParent": False,
                                            "showLink": True,
                                            "extraIcon": "",
                                            "keepAlive": False,
                                            "frameSrc": "",
                                            "frameLoading": False,
                                            "transition": {
                                                "enterTransition": "",
                                                "leaveTransition": ""
                                            },
                                            "hiddenTag": False,
                                            "dynamicLevel": 0,
                                            "auths": [
                                                "list:systemLoginLog",
                                                "delete:systemLoginLog",
                                                "manyDelete:systemLoginLog"
                                            ]
                                        },
                                        "parent": "74defdba-9645-439a-bf36-c0545bb9cda1",
                                        "menu_type": 1,
                                        "is_active": True,
                                        "menu_type_display": "菜单",
                                        "model": [],
                                        "field": []
                                    }
                                ],
                                "count": 2
                            },
                            {
                                "pk": "864eba5d-f793-4a9c-b7eb-cdb227a9d221",
                                "name": "systemNoticeDir",
                                "rank": 68,
                                "path": "/system/notice/",
                                "component": "system/notify/index",
                                "meta": {
                                    "title": "menus.noticeAndAnnouncement",
                                    "icon": "ep:copy-document",
                                    "showParent": False,
                                    "showLink": True,
                                    "extraIcon": "",
                                    "keepAlive": False,
                                    "frameSrc": "",
                                    "frameLoading": False,
                                    "transition": {
                                        "enterTransition": "",
                                        "leaveTransition": ""
                                    },
                                    "hiddenTag": False,
                                    "dynamicLevel": 0,
                                    "auths": []
                                },
                                "parent": "050f7e13-cf60-4c1d-b791-3ab6a97254f6",
                                "menu_type": 0,
                                "is_active": True,
                                "menu_type_display": "目录",
                                "model": [],
                                "field": [],
                                "children": [
                                    {
                                        "pk": "7008bb48-18b1-4bc1-a2ea-c22998024721",
                                        "name": "SystemNotice",
                                        "rank": 69,
                                        "path": "/system/notice/index",
                                        "component": "system/notice/index",
                                        "meta": {
                                            "title": "menus.newsAndAnnouncement",
                                            "icon": "ep:message",
                                            "showParent": False,
                                            "showLink": True,
                                            "extraIcon": "",
                                            "keepAlive": False,
                                            "frameSrc": "",
                                            "frameLoading": False,
                                            "transition": {
                                                "enterTransition": "",
                                                "leaveTransition": ""
                                            },
                                            "hiddenTag": False,
                                            "dynamicLevel": 0,
                                            "auths": [
                                                "list:systemNotice",
                                                "delete:systemNotice",
                                                "manyDelete:systemNotice",
                                                "create:systemNotice",
                                                "update:systemNotice",
                                                "update:systemNoticePublish"
                                            ]
                                        },
                                        "parent": "864eba5d-f793-4a9c-b7eb-cdb227a9d221",
                                        "menu_type": 1,
                                        "is_active": True,
                                        "menu_type_display": "菜单",
                                        "model": [],
                                        "field": []
                                    },
                                    {
                                        "pk": "b8664880-b2dd-48d9-ad88-c79258156084",
                                        "name": "SystemNoticeRead",
                                        "rank": 77,
                                        "path": "/system/notice/read/list",
                                        "component": "system/notice/read/list",
                                        "meta": {
                                            "title": "menus.readNotice",
                                            "icon": "ep:cellphone",
                                            "showParent": False,
                                            "showLink": True,
                                            "extraIcon": "",
                                            "keepAlive": False,
                                            "frameSrc": "",
                                            "frameLoading": False,
                                            "transition": {
                                                "enterTransition": "",
                                                "leaveTransition": ""
                                            },
                                            "hiddenTag": False,
                                            "dynamicLevel": 0,
                                            "auths": [
                                                "list:systemNoticeRead",
                                                "delete:systemNoticeRead",
                                                "manyDelete:systemNoticeRead",
                                                "update:systemNoticeReadState"
                                            ]
                                        },
                                        "parent": "864eba5d-f793-4a9c-b7eb-cdb227a9d221",
                                        "menu_type": 1,
                                        "is_active": True,
                                        "menu_type_display": "菜单",
                                        "model": [],
                                        "field": []
                                    }
                                ],
                                "count": 2
                            },
                            {
                                "pk": "b1a01bd0-e437-4397-8e26-d532a0c04293",
                                "name": "systemFlower",
                                "rank": 82,
                                "path": "/system/flower",
                                "component": "",
                                "meta": {
                                    "title": "menus.timingTask",
                                    "icon": "ep:alarm-clock",
                                    "showParent": False,
                                    "showLink": True,
                                    "extraIcon": "",
                                    "keepAlive": False,
                                    "frameSrc": "/api/flower/",
                                    "frameLoading": False,
                                    "transition": {
                                        "enterTransition": "",
                                        "leaveTransition": ""
                                    },
                                    "hiddenTag": False,
                                    "dynamicLevel": 0,
                                    "auths": [
                                        "list:systemFlower",
                                        "update:systemFlower"
                                    ]
                                },
                                "parent": "050f7e13-cf60-4c1d-b791-3ab6a97254f6",
                                "menu_type": 0,
                                "is_active": True,
                                "menu_type_display": "目录",
                                "model": [],
                                "field": []
                            },
                            {
                                "pk": "53e1896e-dbf1-49aa-85b3-1711e27477ee",
                                "name": "search",
                                "rank": 85,
                                "path": "/system/search",
                                "component": "",
                                "meta": {
                                    "title": "数据查询",
                                    "icon": "ep:data-line",
                                    "showParent": False,
                                    "showLink": False,
                                    "extraIcon": "",
                                    "keepAlive": False,
                                    "frameSrc": "",
                                    "frameLoading": False,
                                    "transition": {
                                        "enterTransition": "",
                                        "leaveTransition": ""
                                    },
                                    "hiddenTag": False,
                                    "dynamicLevel": 0,
                                    "auths": [
                                        "list:systemSearchMenus",
                                        "list:systemSearchRoles",
                                        "list:systemSearchDepts",
                                        "list:systemSearchUsers"
                                    ]
                                },
                                "parent": "050f7e13-cf60-4c1d-b791-3ab6a97254f6",
                                "menu_type": 0,
                                "is_active": True,
                                "menu_type_display": "目录",
                                "model": [],
                                "field": []
                            }
                        ],
                        "count": 9
                    },
                    {
                        "path": "/default/user/info/index",
                        "title": None,
                        "meta": {
                            "title": "menus.personalCenter",
                            "icon": "ep:avatar",
                            "showParent": False,
                            "showLink": True,
                            "extraIcon": "",
                            "keepAlive": False,
                            "frameSrc": "",
                            "frameLoading": False,
                            "transition": {
                                "enterTransition": "",
                                "leaveTransition": ""
                            },
                            "hiddenTag": False,
                            "dynamicLevel": 0,
                            "auths": [
                                "update:UserInfo",
                                "upload:UserInfoAvatar",
                                "update:UserInfoPassword"
                            ]
                        },
                        "children": [
                            {
                                "pk": "6997ffe2-8246-401d-8800-248ecbc2dd83",
                                "name": "UserInfo",
                                "rank": 90,
                                "path": "/user/info/index",
                                "component": "user/info/index",
                                "meta": {
                                    "title": "menus.personalCenter",
                                    "icon": "ep:avatar",
                                    "showParent": False,
                                    "showLink": True,
                                    "extraIcon": "",
                                    "keepAlive": False,
                                    "frameSrc": "",
                                    "frameLoading": False,
                                    "transition": {
                                        "enterTransition": "",
                                        "leaveTransition": ""
                                    },
                                    "hiddenTag": False,
                                    "dynamicLevel": 0,
                                    "auths": [
                                        "update:UserInfo",
                                        "upload:UserInfoAvatar",
                                        "update:UserInfoPassword"
                                    ]
                                },
                                "parent": None,
                                "menu_type": 1,
                                "is_active": True,
                                "menu_type_display": "菜单",
                                "model": [],
                                "field": []
                            }
                        ]
                    },
                    {
                        "path": "/default/user/notice/index",
                        "title": None,
                        "meta": {
                            "title": "menus.messageCenter",
                            "icon": "ep:notification",
                            "showParent": False,
                            "showLink": True,
                            "extraIcon": "",
                            "keepAlive": False,
                            "frameSrc": "",
                            "frameLoading": False,
                            "transition": {
                                "enterTransition": "",
                                "leaveTransition": ""
                            },
                            "hiddenTag": False,
                            "dynamicLevel": 0,
                            "auths": [
                                "list:userNotice",
                                "update:userNoticeRead",
                                "update:userNoticeReadAll"
                            ]
                        },
                        "children": [
                            {
                                "pk": "e9e2e5c4-3735-4219-af09-1e0f3e5118d8",
                                "name": "UserNotice",
                                "rank": 94,
                                "path": "/user/notice/index",
                                "component": "user/notice/index",
                                "meta": {
                                    "title": "menus.messageCenter",
                                    "icon": "ep:notification",
                                    "showParent": False,
                                    "showLink": True,
                                    "extraIcon": "",
                                    "keepAlive": False,
                                    "frameSrc": "",
                                    "frameLoading": False,
                                    "transition": {
                                        "enterTransition": "",
                                        "leaveTransition": ""
                                    },
                                    "hiddenTag": False,
                                    "dynamicLevel": 0,
                                    "auths": [
                                        "list:userNotice",
                                        "update:userNoticeRead",
                                        "update:userNoticeReadAll"
                                    ]
                                },
                                "parent": None,
                                "menu_type": 1,
                                "is_active": True,
                                "menu_type_display": "菜单",
                                "model": [],
                                "field": []
                            }
                        ]
                    },
                ]
            },
            status=status.HTTP_200_OK,
        )
