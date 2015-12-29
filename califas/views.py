#--<encoding:utf8>--
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from califas.models import Director, Title, UserProfile, Friend, Review
from califas.forms import TitleForm, DirectorForm, UserForm, UserProfileForm, ReviewForm

import unidecode
import json
import random
from operator import itemgetter

import ajax_functions

def get_director(director):
	return Directors.get(name=director)


def get_title(title):
	return Title.get(name=title)


def get_average_rating(title):
	all_ratings = Review.objects.filter(title__name=title, rating__gt=0)
	rating_sum = number_of_reviews = average = 0

	for index, rating in enumerate(all_ratings):
		rating_sum += rating.rating
		number_of_reviews = index + 1

	if rating_sum > 0 and number_of_reviews > 0:
		average = rating_sum / number_of_reviews

	return average
	# # Get all the ratings of the title that are greater than 0
	# all_ratings = Review.objects.filter(rating__gt=0)

# Gets the username from the User class and the UserProfile class
def get_user_and_profile(username):
	user_and_profile = {}

	user_name = User.objects.get(username=str(username))
	user_and_profile['name'] = user_name

	user = UserProfile.objects.all()
	# = TODO = Needs a way to only pass the value of the User class if it doesn't find the UserProfile class
	for my_user in user:
		if my_user.usr == user_name:
			user_and_profile['profile'] = my_user

	return user_and_profile


def remove_repeated_titles(titles):
	not_repeated_titles = []
	result = []

	for i in titles:
		try:
			if i['name'] not in not_repeated_titles:
				# append the name
				not_repeated_titles.append(i['name'])
				# append the unrepeated recommendation to a new list
				result.append(i)
		except:
			pass

	return result


def sort_title(titles, field):
	sorted_list = sorted(titles, key=itemgetter(field), reverse=True)

	return sorted_list

def get_movies(movie_filter, qty):
	# all_titles = Title.objects.all()#.order_by('-rating')[:qty]
	all_reviews = Review.objects.all()
	recommendations = []

	for title in movie_filter:
		stringify_title = str(title)
		title_reviews = [p for p in all_reviews if p.title.name==stringify_title]
		opinion = []
		genre = []

		for review in title_reviews:
			opinion.append(review.review)
			genre.append(review.genre)
			poster = review.poster

		rating = get_average_rating(title)

		dict_to_append = {
			'name':     title.name,
			'slug':     title.slug,
			'year':     title.year,
			'director': title.director, # esta me va a dar pedos
			'genre':    genre,
			'opinion':   opinion,
			'rating':   rating,
			'poster':   poster
		}

		recommendations.append(dict_to_append)
		recommendations = sort_title(recommendations, 'rating')

	return remove_repeated_titles(recommendations)[:20]


def get_user_movies(user):
	titles = Title.objects.filter(users=user)
	reviews = Review.objects.filter(user=user)

	reviews_dict = {}
	for y in reviews:
		reviews_dict[str(y.title.name)] = y

	print reviews_dict

	results = []
	try:
		for x in titles:
			movie_details = {
				'name': str(x.name),
				'director': x.director,#directors_dict[str(x)],
				'year': x.year,
				'genre':  [reviews_dict[str(x.name)].genre],
				'rating': reviews_dict[str(x.name)].rating,#['rating'],
				'poster': reviews_dict[str(x.name)].poster,#['poster']
				'opinion': [reviews_dict[str(x.name)].review]
				}

			results.append(movie_details)
	except:
		pass
	print 'results:'
	print results

	return results

###########################################################################

def index(request):
	current_user = str(request.user.username)
	context_dict = {}
	movie_filter = Title.objects.all()
	# if the user is logged in
	if current_user:
		context_dict['titles'] = get_movies(movie_filter, 20)

		return render(request, 'califas/index.html', context_dict)

	else: # if not current_user
		return HttpResponseRedirect('/califas/login')# user is not logged in


# Function to show directors
def show_directors(request):
	current_user = str(request.user.username)
	context_dict = {}
	# if the user is logged in
	if current_user:
		the_user = get_user_and_profile(request.user)

		try:
			directors_list = the_user['profile'].directors.all()
			context_dict['directors_list'] = directors_list
		except:
			context_dict = {'directors_list': ''}

	else:
		return HttpResponseRedirect('/califas/login')# user is NOT logged in

	return render(request, 'califas/directores.html', context_dict)


# I guess this is the function that gives me the bio of the chosen director, if so,
# I must add all the data from the director, even better, pass the object and unwrap it
# in the view.
def director(request, director_name_slug):

 	context_dict ={}
	user = get_user_and_profile(request.user)
	my_director = None

	try:
		directors = user['profile'].directors.all()
		for director in directors:
			if director.slug == director_name_slug:
				my_director = director

		titles = Title.objects.filter(
						director=my_director, user_name=user['name']).order_by('-year')
		context_dict['titles'] = titles
		context_dict['director_name'] = my_director
		context_dict['director_name_slug'] = my_director.director_name_slug
	except:
		print "You have no directors with that name %s " % request.user

	return render(request, 'califas/director.html', context_dict)


@login_required
def add_movie(request):

	if request.method == 'POST':
		director_exists = False
		user = get_user_and_profile(request.user)
		print "user and profile", user
		director_name = request.POST[u'director_name']
		# TODO: make a pop-up if the director doesn't exist in the database
		# get or create director
		director, created = Director.objects.get_or_create(name=director_name)
		# Does the movie exists already?

		valid_title_form = False
		is_a_form = False

		try:
			title_form = Title.objects.get(name=request.POST[u'name'])
			valid_title_form = True
		except:
			title_form = TitleForm(request.POST)
			if title_form.is_valid():
				valid_title_form = True
				is_a_form = True

		review_form = ReviewForm(request.POST, request.FILES)

		# have we been provided with a valid form?
		if (valid_title_form and title_form) and review_form.is_valid():

			review = review_form.save(commit=False)
			# commit only works on forms, not on models
			if is_a_form:
				titulo = title_form.save(commit=False)
			else:
				titulo = title_form

			# Establish a ManyToMany relationship for both director and user
			director.users.add(user['profile'])

			user['profile'].directors.add(director)

			titulo.director = director
			print titulo.director.slug, "FUCK THE SHIT!!!"
			titulo.username = user['name']
			titulo.save()
			titulo.users.add(user['profile'])

			review.poster = request.FILES[u'poster']
			review.user = user['profile']
			review.title = titulo
			print "Con una chingada! ", review.title
			print titulo
			review.save()

		# The supplied form contains errors - just print them to the terminal
		else:
			print "Form ERRORS:"
			print title_form.errors
			print review_form.errors

		directors_list = Director.objects.all()

		return render(request, 'califas/index.html', {'directors_list':directors_list})

	# If the supplied request was not a POST, display the form.
	else:
		title_form = TitleForm()
		review_form = ReviewForm()

		return render(request, 'califas/nueva.html', {'title_form': title_form, 'review_form': review_form})


# Give the detail of the selected movie
def movie_detail(request, director_name_slug, movie_name_slug):

	context_dict = {'director_name': director_name_slug}

	try:
		director = Director.objects.get(slug=director_name_slug)
		titles = Title.objects.filter(user_name=request.user, slug=movie_name_slug).order_by('-year')
		context_dict['titles'] = titles
		context_dict['director_name'] = director
	except Director.DoesNotExist:
		pass

	the_url = 'califas/pelicula.html'
	# What's this for?
	the_url = the_url.replace(' ', '')
	return render(request, the_url, context_dict)

# Check if the user is registered, if so, take him to index, else register him
# = TODO = Change all this function to take the correct validation steps,
# this one is so bad-designed
def registrarse(request):
	registered = False

	if request.method == 'POST':
		# Va a haber dos formas en el registrarse.html, user_form y profile_form
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		print request.POST
		print "WWWWW", request.POST['password']
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			# Now we hash the password with the set_password method.
			user.set_password(user.password)
			user.save()

			profile = profile_form.save(commit=False)
			profile.usr = user
			profile.username = str(profile.usr.username)
			# profile.nombre_usuario = str(profile.usr.username)

			# Here we create the UserProfile's friend table (ManyToMany)
			befriend = Friend()
			befriend.friend_name = user.username
			befriend.save()

			if 'avatar' in request.FILES:
				profile.avatar = request.FILES['avatar']

			# Now we save
			profile.save()

			registered = True

		else:
			print user_form.errors, profile_form.errors

	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	return render(request, 'califas/registrarse.html',
			{'user_form': user_form,
			'profile_form': profile_form,
			'registered': registered} )


def user_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)

		if user:
			if user.is_active:
				login(request, user)
				return  HttpResponseRedirect('/califas/')
			else:
				# An inactive account was used - no loggin in!
				return HttpResponse("Tu cuenta esta desactivada.")
		else:
			print "Invalid login details: {0} {1}".format(username, password)
			return HttpResponse("Invalid login details supplied.")
	else:
		return render(request, 'califas/login.html', {})


@login_required
def user_logout(request):

	logout(request)

	# Pass a "You are now logged out" message.
	return HttpResponseRedirect('/califas/')


def friend_list(request):

	all_users = User.objects.all()
	context_dict = {'all_users': all_users }
	my_friends = UserProfile.objects.all()
	user = User.objects.get(username = request.user)

	for x in my_friends:
		if x.user == user:
			my_friends = x.friends.all()

	amigos = {}
	for y in my_friends:
		amigos[y.friend_name] = y.friend_name

	context_dict['amigos'] = amigos

	return render(request, 'califas/amigos.html', context_dict)


def perfil(request, username):

	user = get_user_and_profile(request.user)
	stalked_user = get_user_and_profile(username)
	perfiles = UserProfile.objects.all()
	mi_perfil = {}
	print "www", stalked_user

	for perfil in perfiles:
		print "----"
		print perfiles
		print perfil
		print "w", stalked_user['profile']
		if perfil.usr == stalked_user['profile'].usr:
			mi_perfil['user'] = perfil.usr
			mi_perfil['website'] = perfil.website
			mi_perfil['picture'] = perfil.avatar
			mi_perfil['about'] = perfil.about

	# Las 3 peliculas favoritas del usuario
	directors = stalked_user['profile'].directors.all()

	#directors = Director.objects.filter(user_name=username) # .Title.objects.all()
	movies = Title.objects.filter(users=stalked_user['name'])

	print "Mis pelis: ", movies

	context_dict = {
		'mi_perfil': mi_perfil,
		'directors': directors,
		'favorite_movies': movies
	}

	return render(request, 'califas/perfil.html', context_dict)


#This function must send a friendship request to the target user.
def befriend(request):

	usuario = str(request.GET[u'usuario'])
	amigarse = request.GET[u'amigarse']

	next_friend = Friend.objects.all()
	print "next_friend:" , next_friend
	for a in next_friend:
		if a.friend_name == amigarse:
			# WTF why change the var in the middle of a loop??? Test this with changes
			next_friend = a
			break

	user = UserProfile.objects.all()

	for x in user:
		if x.user.username == usuario:
			usuario = x
			next_friend.save()
			x.friends.add(next_friend)
			x.save()

		else:
			print "no"

	return HttpResponseRedirect('/califas/amigos')


# Is this function supposed to give the director's bio?
# There's already another one above doing the same!
def chosen_director_filmography(request, director_name_slug):

	context_dict = {}

	director = Director.objects.get(slug=director_name_slug)
	if director:
		context_dict['director'] = director

	filmography = Title.objects.filter(director=director)
	context_dict['filmography'] = filmography

	return render(request, 'califas/bio.html', context_dict)


# The action is in the AJAX!
def epocas(request):
	return render(request, 'califas/epocas.html', {})


# exitos
def get_movies_by_rating(request):
	movie_filter = Title.objects.all()
	titles = get_movies(movie_filter, 20)

	return render(request, 'califas/exitos.html', {'titles': titles})


@login_required
def user_movies(request):
	the_user = get_user_and_profile(request.user)
	print the_user['profile']
	titles = get_user_movies(the_user['profile'])
	print "titles: "
	print ">>>>>>>>>>>>>>>>>>>>>>>",titles[0]

	return render(request, 'califas/mis_peliculas.html', {'titles': titles})


def stats(request):
	context_dict = {}
	current_user = str(request.user.username)

	if current_user:
		the_user = get_user_and_profile(request.user)
	else:
		return render(request, 'califas/index.html', {})

	if the_user:
		titles_query = Title.objects.all().filter(user_name=the_user['name'])
		# cuantas peliculas ha visto el usuario
		context_dict['vistas'] = len(titles_query)
		context_dict['fav_gen'] = titles_query.order_by('genre')

		fav_gen = {}
		for i in context_dict['fav_gen']:
			if str(i.genre) not in fav_gen:
				fav_gen[str(i.genre)] = 1
			else:
				fav_gen[str(i.genre)] += 1
		# estudiar esta linea que no le entiendo bien
		user_fav_gen = max(fav_gen.iterkeys(), key = lambda k: fav_gen[k])
		context_dict['user_fav_gen'] = [user_fav_gen, fav_gen[user_fav_gen]]

	return render(request, 'califas/stats.html', {'stats': context_dict})
