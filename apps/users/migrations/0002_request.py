# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-11-21 20:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests_sent', to='users.User')),
                ('request_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests_received', to='users.User')),
            ],
        ),
    ]