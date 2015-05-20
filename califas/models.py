from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone

class Director(models.Model):

	nationality = models.CharField(max_length=50, blank=True)
	director_name = models.CharField(max_length=128, unique=True)
	slug = models.SlugField(unique=True) 

	biography = models.TextField(max_length=500)
	birth = models.IntegerField(default=0)
	death = models.IntegerField(default=0)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.director_name) 
		super(Director, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.director_name


class Title(models.Model):

	user_name = models.ForeignKey(User)
	director = models.ForeignKey(Director)
	movie_name = models.CharField(max_length=128)
	slug = models.SlugField(unique=False)
	year = models.IntegerField(default=1900)
	genre = models.CharField(max_length=100)
	review = models.TextField(max_length=300)
	rating = models.IntegerField(default=0)
	poster = models.ImageField(upload_to='movie_images', blank=True)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.movie_name + '-' + str(self.year))
		super(Title, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.movie_name


class Friend(models.Model):

	friend_name = models.CharField(max_length=100, default='', unique=True)
	member_since = models.DateField(default=timezone.now())

	def __unicode__(self):
		return self.friend_name


class UserProfile(models.Model):

	user = models.OneToOneField(User)
	nombre_usuario = models.CharField(max_length=50)
	real_name = models.CharField(max_length=128, blank=True)
	last_name = models.CharField(max_length=128, blank=True)
	age = models.IntegerField(default=0)
	website = models.URLField(blank=True)
	picture = models.ImageField(upload_to='profile_images', blank=True)
	about_user = models.TextField(max_length=155, blank=True)
	friends = models.ManyToManyField(Friend, blank=True)
	directors = models.ManyToManyField(Director, blank=True)

	def __unicode__(self):
		return self.user.username


