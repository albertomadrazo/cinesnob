#--<encoding:utf8>--

from django.conf.urls import patterns, url
from califas import views
from califas import ajax_functions

urlpatterns = patterns('',
		url(r'^$', views.index, name='index'), # director_name_url es el 2do parametro
		# de la funcion director() en view
		url(r'^director/(?P<director_name_slug>[\w\-]+)/$', views.director, name='director'),
		url(r'^nueva/$', views.add_movie, name='nueva'),
		url(r'^pelicula/(?P<director_name_slug>[\w\-]+)/(?P<movie_name_slug>[\w\-]+)$', views.movie_detail, name='pelicula'),
		url(r'^registrarse/$', views.registrarse, name='registrarse'),
		url(r'^login/$', views.user_login, name='user_login'),
		url(r'^logout/$', views.user_logout, name='user_logout'),
		url(r'^amigos/$', views.friend_list, name='friend_list'),
		url(r'^perfil/(?P<username>[\w\-]+)$', views.perfil, name='perfil'),
		url(r'^befriend/$', views.befriend, name='befriend'),
		url(r'^bio/(?P<director_name_slug>[\w\-]+)/$', views.chosen_director_filmography, name='biografia'),
		url(r'^epocas/$', views.epocas, name='epocas'),
		url(r'^get_movies_by_age/$', ajax_functions.get_movies_by_age, name='get_movies_by_age'),
		url(r'^delete_title/$', ajax_functions.delete_title, name='delete_title'),
		url(r'^directores/$', views.show_directors, name='directores'),
		url(r'^exitos/$', views.get_movies_by_rating, name='exitos'),
		url(r'^stats/$', views.stats, name='stats'),
		url(r'^mis_peliculas/$', views.user_movies, name='user_movies'),
	)