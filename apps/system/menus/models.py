from django.db import models
from django.utils.translation import gettext_lazy as _


class Menu(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("名称"))
    code = models.CharField(max_length=100, unique=True, verbose_name=_("编码"))
    type = models.CharField(max_length=50, verbose_name=_("类型"))
    parentId = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children", verbose_name=_("父级菜单")
    )
    path = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("路径"))
    icon = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("图标"))
    component = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("组件"))
    order = models.IntegerField(default=0, verbose_name=_("排序"))
    show = models.BooleanField(default=True, verbose_name=_("显示"))
    enable = models.BooleanField(default=True, verbose_name=_("启用"))
    layout = models.CharField(null=True, blank=True, max_length=50, verbose_name=_("布局"))
    keepAlive = models.BooleanField(default=False, verbose_name=_("KeepAlive"))

    def __str__(self):
        return self.name
