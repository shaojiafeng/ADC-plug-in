# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-28 11:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0005_salerank'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='openid',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='微信唯一ID'),
        ),
    ]