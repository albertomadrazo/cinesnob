from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Director(models.Model):

	user_name = models.ForeignKey(User)
	#user = models.ForeignKey(User)

	director_name = models.CharField(max_length=128, unique=True)
	slug = models.SlugField(unique=True)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.director_name)
		super(Director, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.director_name


class Title(models.Model):
	director = models.ForeignKey(Director)
	movie_name = models.CharField(max_length=128)
	slug = models.SlugField(unique=False) # No se aqui, si dos peliculas se llaman igual...
	year = models.IntegerField(default=1900)
	genre = models.CharField(max_length=100)
	review = models.TextField(max_length=300)
	rating = models.IntegerField(default=0)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.movie_name)
		super(Title, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.movie_name


class Friend(models.Model):
	username = models.ForeignKey(User)
	friend_name = models.CharField(max_length=128)
	date_added = models.DateField()

	def __unicode__(self):
		return self.friend_name


class UserProfile(models.Model):
	user = models.OneToOneField(User)
	website = models.URLField(blank=True)
	picture = models.ImageField(upload_to='profile_images', blank=True)
	about_user = models.TextField(max_length=155, blank=True)
	#friends = models.ManyToManyField('self')

	def __unicode__(self):
		return self.user.username


