from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone

from unidecode import unidecode


# model UserProfile > one to one < User
class UserProfile(models.Model):

	username = models.CharField(max_length=50)
	name models.CharField(max_length=100)
	email = models.EmailField(max_length=100)
	website = models.URLField(blank=True)
	about = models.TextField(max_length=200, blank=True)
	avatar = models.ImageField(upload_to='profile_images', default='default.jpg')

	# The model's relationships with other tables
	usr = models.OneToOneField(User)
	directors = models.ManyToManyField(Director, blank=True)
	friends = models.ManyToManyField(Friend, blank=True)

	def __unicode__(self):
		return self.user.username


# model Director > one to many (Title),
#		Director > many to many < UserProfile
class Director(models.Model):

	nationality = models.CharField(max_length=50, blank=True)
	name = models.CharField(max_length=128, unique=True)
	slug = models.SlugField(unique=True) 
	about = models.TextField(max_length=500)
	birth = models.IntegerField(default=0)
	death = models.IntegerField(default=0)
	picture = models.ImageField(upload_to='director_images', default='default.jpg')

	# The model's relationships with other tables
	users = models.ManyToManyField(UserProfile, blank=True)

	def save(self, *args, **kwargs):
		self.slug = slugify(unidecode(self.director_name)) 
		super(Director, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.name


# model Title 
class Title(models.Model):

	name = models.CharField(max_length=128)
	slug = models.SlugField(unique=False)
	year = models.IntegerField(default=1900)

	# The model's relationships with other tables
	users = models.ManyToManyField(blank=True)
	director = models.ForeignKey(Director)

	def save(self, *args, **kwargs):
		self.slug = slugify(unidecode(self.movie_name) + '-' + str(self.year))
		super(Title, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.movie_name


class Review(models.Model):

	genre = models.CharField(max_length=100)
	review = models.TextField(max_length=300)
	rating = models.IntegerField(default=0)
	poster = models.ImageField(upload_to='movie_images', blank=True)

	# The model's relationships with other tables
	user = models.ForeignKey(UserProfile)
	title = models.ForeignKey(Title)

	def __unicode__(self):
		return self.title


# model Friend > many to many
class Friend(models.Model):

	friends = models.ManyToManyField(UserProfile)
	member_since = models.DateField(default=timezone.now())