# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nationality', models.CharField(max_length=50, blank=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('slug', models.SlugField(unique=True)),
                ('about', models.TextField(max_length=500)),
                ('birth', models.IntegerField(default=0)),
                ('death', models.IntegerField(default=0)),
                ('picture', models.ImageField(default=b'default.jpg', upload_to=b'director_images')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('member_since', models.DateField(default=datetime.datetime(2015, 12, 3, 3, 27, 31, 809539, tzinfo=utc))),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('genre', models.CharField(max_length=100)),
                ('review', models.TextField(max_length=300)),
                ('rating', models.IntegerField(default=0)),
                ('poster', models.ImageField(upload_to=b'movie_images', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('slug', models.SlugField()),
                ('year', models.IntegerField(default=1900)),
                ('director', models.ForeignKey(to='califas.Director')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('website', models.URLField(blank=True)),
                ('about', models.TextField(max_length=200, blank=True)),
                ('avatar', models.ImageField(default=b'default.jpg', upload_to=b'profile_images')),
                ('directors', models.ManyToManyField(to='califas.Director', blank=True)),
                ('friends', models.ManyToManyField(to='califas.Friend', blank=True)),
                ('usr', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='title',
            name='users',
            field=models.ManyToManyField(to='califas.UserProfile', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='review',
            name='title',
            field=models.ForeignKey(to='califas.Title'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='review',
            name='user',
            field=models.ForeignKey(to='califas.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='friend',
            name='friends',
            field=models.ManyToManyField(to='califas.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='director',
            name='users',
            field=models.ManyToManyField(to='califas.UserProfile', blank=True),
            preserve_default=True,
        ),
    ]
