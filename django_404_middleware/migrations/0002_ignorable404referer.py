# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2019-04-08 06:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_404_middleware', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ignorable404Referer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pattern', models.TextField(help_text='Referers matching this pattern are ignored.')),
                ('exact', models.BooleanField(default=True, verbose_name='The full referer must match')),
                ('is_re', models.BooleanField(default=False, verbose_name='Is regular expression')),
                ('case_sensitive', models.BooleanField(default=False, verbose_name='Is case sensitive')),
            ],
            options={
                'verbose_name': 'Ignorable 404 Referer',
            },
        ),
    ]
