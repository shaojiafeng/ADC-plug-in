# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-15 08:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_auto_20171215_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='ut',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app01.UserType'),
        ),
    ]