# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-11-21 21:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20181121_1321'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='request',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='request',
            name='updated_at',
        ),
    ]
