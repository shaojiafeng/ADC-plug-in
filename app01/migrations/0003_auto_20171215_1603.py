# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-15 08:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('xxx', models.CharField(max_length=32, verbose_name='类型名称')),
            ],
        ),
        migrations.AddField(
            model_name='userinfo',
            name='email',
            field=models.EmailField(default='123@live.com', max_length=32, verbose_name='邮箱'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='pwd',
            field=models.CharField(default='111', max_length=32, verbose_name='密码'),
        ),
        migrations.AlterField(
            model_name='role',
            name='caption',
            field=models.CharField(max_length=32, verbose_name='角色名称'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='name',
            field=models.CharField(max_length=32, verbose_name='用户名称'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='ut',
            field=models.ForeignKey(default=34, on_delete=django.db.models.deletion.CASCADE, to='app01.UserType'),
            preserve_default=False,
        ),
    ]