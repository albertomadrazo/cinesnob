#--<coding:utf8-->
from django import forms
from django.contrib.auth.models import User

from califas.models import Title, Director, UserProfile, Review

GENRE_CHOICES = (('accion', 'Acción'),
				 ('terror', 'Terror'),
				 ('drama', 'Drama'),
				 ('comedia', 'Comedia'),
				 ('otro', 'Otro'),)

RATINGS = (('1', ''),
		   ('2', ''),
		   ('3', ''),
		   ('4', ''),
		   ('5', ''),)


class DirectorForm(forms.ModelForm):
	name = forms.CharField(max_length=128, help_text='Director')
	about = forms.TextField(max_length=1500, help_text='Cuéntanos acerca de este director')
	birth = forms.IntegerField()
	death = forms.IntegerField()
	picture = forms.ImageField()

	class Meta:
		model Director


class TitleForm(forms.ModelForm):
	name = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'placeholder':'película'}))
	year = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':'año'}))

	class Meta:
		model = Title
		fields= ('name', 'year',)


class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model User
		fields = ('username', 'email', 'password',)


class UserProfileForm(forms.ModelForm):

	class Meta:
		model = UserProfile
		fields = ('name', 'email', 'website', 'about', 'avatar',)