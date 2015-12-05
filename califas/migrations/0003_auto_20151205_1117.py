# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('califas', '0002_auto_20150506_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friend',
            name='friend_name',
            field=models.CharField(default=b'', max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='friend',
            name='member_since',
            field=models.DateField(default=datetime.datetime(2015, 12, 5, 17, 17, 22, 60176, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
