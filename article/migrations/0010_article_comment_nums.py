# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-07 14:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0009_auto_20170407_2240'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='comment_nums',
            field=models.IntegerField(default=0),
        ),
    ]
