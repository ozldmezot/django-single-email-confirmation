# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-27 14:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('single_email', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailaddress',
            name='key',
            field=models.TextField(blank=True, null=True, unique=True),
        ),
    ]