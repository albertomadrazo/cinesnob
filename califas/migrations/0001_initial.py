# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nationality', models.CharField(default=b'gringo', max_length=50)),
                ('director_name', models.CharField(unique=True, max_length=128)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('friend_name', models.CharField(default=b'', unique=True, max_length=100)),
                ('is_friend', models.BooleanField(default=False)),
                ('date_added', models.DateField(default=datetime.datetime(2015, 4, 10, 9, 16, 2, 515237, tzinfo=utc))),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('movie_name', models.CharField(max_length=128)),
                ('slug', models.SlugField()),
                ('year', models.IntegerField(default=1900)),
                ('genre', models.CharField(max_length=100)),
                ('review', models.TextField(max_length=300)),
                ('rating', models.IntegerField(default=0)),
                ('director', models.ForeignKey(to='califas.Director')),
                ('user_name', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre_usuario', models.CharField(max_length=50)),
                ('real_name', models.CharField(default=b'anonymous', max_length=128)),
                ('last_name', models.CharField(default=b'anonymous', max_length=128)),
                ('age', models.IntegerField(default=0)),
                ('website', models.URLField(blank=True)),
                ('picture', models.ImageField(upload_to=b'profile_images', blank=True)),
                ('about_user', models.TextField(max_length=155, blank=True)),
                ('directors', models.ManyToManyField(to='califas.Director')),
                ('friends', models.ManyToManyField(to='califas.Friend')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
