# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2022-05-07 15:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallet',
            name='disabled_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
