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
            model_name='friend',
            name='member_since',
            field=models.DateField(default=datetime.datetime(2015, 5, 7, 2, 45, 7, 247205, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='title',
            name='poster',
            field=models.ImageField(upload_to=b'movie_images', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(upload_to=b'profile_images', blank=True),
            preserve_default=True,
        ),
    ]
