from django.contrib.auth.models import Group
from django.db import models
from django.utils.translation import gettext_lazy as _


class Role(Group):
    code = models.CharField(max_length=100, unique=True, verbose_name=_("角色编码"))
    order = models.IntegerField(default=0, verbose_name=_("排序"))
    enable = models.BooleanField(default=True, verbose_name=_("启用"))
    description = models.TextField(blank=True, null=True, verbose_name=_("描述"))

    def __str__(self):
        return self.code
