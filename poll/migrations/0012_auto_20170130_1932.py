# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-30 19:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0011_auto_20170130_1922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='page_type',
            field=models.CharField(choices=[('Question', 'Question'), ('Video', 'Video'), ('Starting', 'Starting'), ('Login', 'Login'), ('Lottery', 'Lottery')], max_length=50),
        ),
    ]
