#--<coding:utf8-->
from django import forms
from califas.models import Title, Director, UserProfile
from django.contrib.auth.models import User

GENRE_CHOICES = (('accion','Acción'),
				 ('terror', 'Terror'),
				 ('drama', 'Drama'),
				 ('comedia', 'Comedia'),
				 ('otro', 'Otro'), )

RATINGS = ( ('1',''),
			('2',''),
			('3',''),
			('4',''),
			('5',''), )

class DirectorForm(forms.ModelForm):
	director_name = forms.CharField(max_length=128, help_text='Director')

	# An inline class to provide additional information on the form.
	class Meta:
		# Provide an association between the ModelForm and the model.
		model = Director


class TitleForm(forms.ModelForm):
	movie_name = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'placeholder': 'película'}))
	year = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'año'}))
	genre = forms.CharField(widget=forms.Select(choices=GENRE_CHOICES, attrs={'id':'opciones'}))
	review = forms.CharField(widget=forms.Textarea, max_length=300, help_text='comentarios')
	rating = forms.ChoiceField(widget=forms.RadioSelect(attrs={'id':'estrellas'}), choices=RATINGS, initial=0 )
	poster = forms.FileField()
	class Meta:
		model = Title

		# What fields do we want to include in our form?
		# This way we don't need every field in the model present
		# Some fields may allow NULL values, so we may not want to include them
		# Here, we are hiding the foreign key.
		fields = ('movie_name', 'year', 'genre', 'review', 'rating', 'poster')
		# en la forma que se hace tengo que crear el director, pero no le estoy poniendo
		# el campo, supongo que se puede resolver con un campo normal de html y despues usar
		# esa info para primero crear el director y despues crear el titulo con todo lo demas
		# if director: meter todos los datos del titulo al director ya existente.

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
	class Meta:
		model=UserProfile
		fields = ('real_name', 'last_name', 'age', 'website', 'picture', 'about_user')