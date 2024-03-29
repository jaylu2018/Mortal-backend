# Generated by Django 4.2.6 on 2023-12-20 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0002_role_enable'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='头像'),
        ),
        migrations.AddField(
            model_name='user',
            name='enable',
            field=models.BooleanField(default=True, verbose_name='启用'),
        ),
        migrations.AddField(
            model_name='user',
            name='genders',
            field=models.CharField(choices=[('0', '男'), ('1', '女')], default='0', max_length=1, verbose_name='性别'),
        ),
        migrations.AddField(
            model_name='user',
            name='roles',
            field=models.ManyToManyField(related_name='users', to='roles.role'),
        ),
    ]
