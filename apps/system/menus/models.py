class Menu(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=50)
    parentId = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    path = models.CharField(max_length=255, null=True, blank=True)
    icon = models.CharField(max_length=100, null=True, blank=True)
    component = models.CharField(max_length=255, null=True, blank=True)
    order = models.IntegerField(default=0)
    show = models.BooleanField(default=True)
    enable = models.BooleanField(default=True)
    layout = models.CharField(null=True, blank=True, max_length=50)
    keepAlive = models.BooleanField(default=False)

    def __str__(self):
        return self.name
