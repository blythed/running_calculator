# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-29 06:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0003_auto_20160329_0618'),
    ]

    operations = [
        migrations.AddField(
            model_name='athlete',
            name='gender',
            field=models.CharField(default='Male', max_length=6),
        ),
    ]