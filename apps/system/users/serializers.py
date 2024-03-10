from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from django.utils.translation import gettext_lazy as _

from system.roles.models import Role
from system.roles.serializers import RoleSerializer
from system.users.models import User


# 自定义登录序列化器，继承自TokenObtainPairSerializer
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["token"] = data.pop("access")
        return data


# Token刷新序列化器
class MyTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["token"] = data.pop("access")
        return data


# 注册序列化器
class UserRegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(
        label=_("确认密码"),
        help_text=_("确认密码"),
        min_length=4,
        max_length=20,
        write_only=True,
        error_messages={"min_length": _("密码长度小于4位"), "max_length": _("密码长度大于20位")},
    )

    class Meta:
        model = User
        fields = ("id", "username", "password", "password_confirm", "email", "mobile")
        # 对于模型中已经存在的字段，可以通过extra_kwargs扩展一下额外的限制
        extra_kwargs = {
            "username": {
                "label": _("用户名"),
                "help_text": _("用户名"),
                "min_length": 4,
                "max_length": 20,
                "error_messages": {"min_length": _("用户名长度小于4位"), "max_length": _("用户名长度大于20位")},
            },
            "password": {
                "label": _("密码"),
                "help_text": _("密码"),
                "min_length": 4,
                "max_length": 20,
                "write_only": True,
                "error_messages": {"min_length": _("密码长度小于6位"), "max_length": _("密码长度大于20位")},
            },
            "email": {"label": _("邮箱"), "help_text": _("邮箱"), "write_only": True},
            "mobile": {"label": _("手机号"), "help_text": _("手机号"), "write_only": True},
        }

    # 对于模型中不存在的字段，可以通过validate_<字段名>方法来扩展
    def validate_password_confirm(self, value):
        password = self.initial_data.get("password")
        if password != value:
            raise serializers.ValidationError(_("两次密码不一致"))
        return value

    # 重写create方法，对密码进行加密
    def create(self, validated_data):
        validated_data.pop("password_confirm")
        user = super().create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


# 用户序列化器，包含创建用户和更新用户
class UserSerializer(serializers.ModelSerializer):
    roleIds = serializers.PrimaryKeyRelatedField(
        source="roles", many=True, queryset=Role.objects.all(), write_only=True
    )
    roles = RoleSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "mobile", "password", "avatar", "enable", "gender", "roles", "roleIds")
        extra_kwargs = {
            "username": {
                "label": _("用户名"),
                "help_text": _("用户名"),
                "min_length": 4,
                "max_length": 20,
                "error_messages": {"min_length": _("用户名长度小于4位"), "max_length": _("用户名长度大于20位")},
            },
            "password": {
                "label": _("密码"),
                "help_text": _("密码"),
                "min_length": 4,
                "max_length": 20,
                "write_only": True,
                "error_messages": {"min_length": _("密码长度小于6位"), "max_length": _("密码长度大于20位")},
            },
        }

    # 重写create方法，对密码进行加密
    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    # 重写update方法，对密码进行更新
    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)  # 如果没有传递password，则不更新密码
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
