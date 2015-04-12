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
            name='date_added',
            field=models.DateField(default=datetime.datetime(2015, 4, 11, 18, 2, 54, 795198, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
