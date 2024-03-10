from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from system.roles.models import Role


class User(AbstractUser):
    """
    用户
    """

    name = models.CharField(
        max_length=30, null=True, blank=True, verbose_name=_("姓名")
    )  # 用户可能不希望他们的用户名被公开，因此将用户的姓名和用户名分开
    gender = models.CharField(max_length=1, choices=(("1", "男"), ("2", "女")), default="1", verbose_name=_("性别"))
    mobile = models.CharField(max_length=11, verbose_name=_("电话"))
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name=_("邮箱"))
    avatar = models.CharField(max_length=200, null=True, blank=True, verbose_name=_("头像"))
    enable = models.BooleanField(default=True, verbose_name=_("启用"))
    roles = models.ManyToManyField(Role, blank=True, related_name="users")

    class Meta:
        db_table = "tb_users"
        verbose_name = _("用户")
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    REQUIRED_FIELDS = ["mobile"]  # 再通过createsuperuser 管理命令创建用户时，会提示输入mobile字段
