# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-25 00:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='template_id',
            field=models.IntegerField(blank=True, default=-1, verbose_name='Template ID'),
        ),
        migrations.AlterField(
            model_name='page',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='Assignee Email'),
        ),
        migrations.AlterField(
            model_name='page',
            name='url',
            field=models.CharField(max_length=500),
        ),
    ]
