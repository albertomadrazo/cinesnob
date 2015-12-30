# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('califas', '0002_auto_20151219_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friend',
            name='member_since',
            field=models.DateField(default=datetime.datetime(2015, 12, 30, 2, 59, 15, 516011, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
