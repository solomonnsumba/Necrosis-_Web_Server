# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-07-26 11:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('necrosis', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Api_Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(upload_to='api_uploads/')),
            ],
        ),
    ]
