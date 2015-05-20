#--<encoding:utf8>--

from django.conf.urls import patterns, url
from califas import views

urlpatterns = patterns('',
		url(r'^$', views.index, name='index'), # director_name_url es el 2do parametro
		# de la funcion director() en view
		url(r'^director/(?P<director_name_slug>[\w\-]+)/$', views.director, name='director'),
		url(r'^nueva/$', views.nueva, name='nueva'),
		url(r'^base/$', views.base, name='base'),
		url(r'^pelicula/(?P<director_name_slug>[\w\-]+)/(?P<movie_name_slug>[\w\-]+)$', views.pelicula, name='pelicula'),
		url(r'^registrarse/$', views.registrarse, name='registrarse'),
		url(r'^login/$', views.user_login, name='user_login'),
		url(r'^logout/$', views.user_logout, name='user_logout'),
		url(r'^amigos/$', views.friend_list, name='friend_list'),
		url(r'^perfil/(?P<username>[\w\-]+)$', views.perfil, name='perfil'),
		url(r'^befriend/$', views.befriend, name='befriend'),
		url(r'^bio/(?P<director_name_slug>[\w\-]+)/$', views.biografia, name='biografia'),
		url(r'^epocas/$', views.epocas, name='epocas'),
		url(r'^get_movies_by_age/$', views.get_movies_by_age, name='get_movies_by_age'),
		url(r'^directores/$', views.directores, name='directores'),
		url(r'^exitos/$', views.get_movies_by_rating, name='exitos'),
)		