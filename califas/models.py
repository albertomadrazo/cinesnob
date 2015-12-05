from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone

from unidecode import unidecode


# model UserProfile > one to one < User
class UserProfile(models.Model):

	username = models.CharField(max_length=50)
	name = models.CharField(max_length=100)
	email = models.EmailField(max_length=100)
	website = models.URLField(blank=True)
	about = models.TextField(max_length=200, blank=True)
	avatar = models.ImageField(upload_to='profile_images', default='default.jpg')

	# The model's relationships with other tables
	usr = models.OneToOneField(User)
	directors = models.ManyToManyField('Director', blank=True)
	friends = models.ManyToManyField('Friend', blank=True)

	def __unicode__(self):
		return self.usr.username


# model Title 
class Title(models.Model):

	name = models.CharField(max_length=128, unique=True)
	slug = models.SlugField(unique=True)
	year = models.IntegerField(default=1900)

	# The model's relationships with other tables
	users = models.ManyToManyField('UserProfile', blank=True)
	director = models.ForeignKey('Director')

	def save(self, *args, **kwargs):
		try:
			self.name = unidecode(unicode(self.name, "utf-8"))
		except:
			self.name = unidecode(self.name)
			
		self.slug = slugify(self.name+'-'+str(self.year))
		super(Title, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.name # not necessary, maybe it's better to retrieve Director


class Review(models.Model):

	genre = models.CharField(max_length=100)
	review = models.TextField(max_length=1000)
	rating = models.IntegerField(default=0)
	poster = models.ImageField(upload_to='movie_images')

	# The model's relationships with other tables
	user = models.ForeignKey('UserProfile')
	title = models.ForeignKey('Title')

	def __unicode__(self):
		return unicode(self.title)


# model Friend > many to many
class Friend(models.Model):

<<<<<<< HEAD
	friends = models.ManyToManyField('UserProfile')
=======
	friend_name = models.CharField(max_length=100, default='')
>>>>>>> See no advance here...
	member_since = models.DateField(default=timezone.now())


# model Director > one to many (Title),
#		Director > many to many < UserProfile
class Director(models.Model):

	nationality = models.CharField(max_length=50, blank=True)
	name = models.CharField(max_length=128, unique=True)
	slug = models.SlugField(unique=True) 
	about = models.TextField(max_length=2000)
	birth = models.IntegerField(default=0)
	death = models.IntegerField(default=0)
	picture = models.ImageField(upload_to='director_images', default='default.jpg')

	# The model's relationships with other tables
	users = models.ManyToManyField(UserProfile, blank=True)

<<<<<<< HEAD
	def save(self, *args, **kwargs):
		try:
			self.name = unidecode(unicode(self.name, "utf-8")).encode("utf-8")
		except:

			self.name = unidecode(self.name)
		self.slug = slugify(self.name) 
		super(Director, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.name
=======
	def __unicode__(self):
		return self.user.username
>>>>>>> See no advance here...
