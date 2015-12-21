# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('califas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='director',
            name='about',
            field=models.TextField(max_length=2000),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='friend',
            name='member_since',
            field=models.DateField(default=datetime.datetime(2015, 12, 19, 19, 41, 8, 331354, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='review',
            name='poster',
            field=models.ImageField(upload_to=b'movie_images'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='review',
            name='review',
            field=models.TextField(max_length=1000),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='title',
            name='name',
            field=models.CharField(unique=True, max_length=128),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='title',
            name='slug',
            field=models.SlugField(unique=True),
            preserve_default=True,
        ),
    ]
