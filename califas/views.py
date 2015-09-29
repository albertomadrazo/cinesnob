#--<encoding:utf8>--
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from califas.models import Director, Title, UserProfile, Friend
from califas.forms import TitleForm, DirectorForm, UserForm, UserProfileForm
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

import json

# Gets the username from the User class and the UserProfile class
def get_user_and_profile(username):

	user_and_profile = {}

	user_name = User.objects.get(username=str(username))
	user_and_profile['name'] = user_name

	user = UserProfile.objects.all()

	# = TODO = Needs a way to only pass the value of the User class if it doesn't find the UserProfile class
	for my_user in user:
		if my_user.user == user_name:
			user_and_profile['profile'] = my_user
			return user_and_profile

	return None


def index(request):

	current_user = str(request.user.username)
	context_dict = {}

	# if the user is logged in
	if current_user:
		# the_user = get_user_and_profile(request.user)
		# try:
		# 	directors_list = the_user['profile'].directors.all() 
		# 	context_dict = {'directors_list': directors_list}
		# except:
		# 	context_dict = {'directors_list': ''}
		recommendations = Title.objects.all().order_by('-rating')[:6]
		context_dict['recommendations'] = recommendations	

		return render(request, 'califas/index.html', context_dict)

	else:
		return HttpResponseRedirect('/califas/login')# if the user is not logged in

# Function to show directors
def show_directors(request):

	current_user = str(request.user.username)
	context_dict = {}
	# if the user is logged in
	if current_user:
		the_user = get_user_and_profile(request.user)
		try:
			# Is this getting only the directors belonging to this specific user?
			# What I want (I think I remember) is all the directors.
			directors_list = the_user['profile'].directors.all() 
			context_dict['directors_list'] = directors_list
		except:
			context_dict = {'directors_list': ''}

	else:
		return HttpResponseRedirect('/califas/login')# if the user is NOT logged in

	return render(request, 'califas/directores.html', context_dict)

# What's the raison d'ëtre of this function?
def base(request):

	context = RequestContext(request)
	context_dict ={'uno': 1}

	return render(request, 'califas/base.html', context_dict)

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

		director_name = request.POST[u'director_name']
	
		title_form = TitleForm(request.POST, request.FILES)

		#title_form.poster = request.FILES['poster']
		print "$$$$$$$$$$", title_form
		# title_form.save(commit=False)
		# have we been provided with a valid form?
		if title_form.is_valid():
			print "*"
			nuevo_titulo = title_form.save(commit=False)
			nuevo_titulo.user_name = user['name']

			try:
				director = user['profile'].directors.get(director_name=director_name)
			except:
				director_list = Director.objects.all()

				for director in director_list:
					print director.director_name, director_name

					if director.director_name == director_name:
						director_exists = True

				# If the director was not found, create it
				if director_exists == False:	
					director = Director(director_name=director_name)
					director.save()
	
				user['profile'].directors.add(director)

			nuevo_titulo.director = director
			nuevo_titulo.poster = request.FILES['poster']
			nuevo_titulo.save()
#			# Now call the index() view.
#			# The user will be shown the homepage.
#			return index(request)
		else:
			print "**"

#			# The supplied form contains errors - just print them to the terminal
			print title_form.errors

		directors_list = user['profile'].directors.all() #funciones.call_directors()
		#url = HttpResponseRedirect(reverse('view.index'))
		#return render_to_response('califas/', directors_list, context) #HttpResponseRedirect('/califas/index.html')
		return render(request, 'califas/index.html', {'directors_list':directors_list})

	# If the supplied request was not a POST, display the form.
	else:
		title_form = TitleForm()

	# Bad form (or no details), no form supplied...
	# Render the form with error messages(if any).
		
		return render(request, 'califas/nueva.html', {'title_form': title_form})


# en esta view, vamos a dar el detalle de la pelicula seleccionada
# This should be requested via AJAX.
def movie_detail(request, director_name_slug, movie_name_slug):

	print "PELICULA.VIEW"
	#movie_name = movie_name_detail.replace('_', ' ')
	#director_name = director_name_url.replace('_', ' ')
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

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			# Now we hash the password with the set_password method.
			user.set_password(user.password)

			user.save()
			profile = profile_form.save(commit=False)

			profile.user = user
			profile.nombre_usuario = str(profile.user.username)

			# Here we create the UserProfile's friend table (ManyToMany)
			befriend = Friend()
			befriend.friend_name = user.username
			befriend.save()

			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']

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
		if perfil.user == stalked_user['profile'].user:
			mi_perfil['user'] = perfil.user
			mi_perfil['website'] = perfil.website
			mi_perfil['picture'] = perfil.picture
			mi_perfil['about'] = perfil.about_user

	# Las 3 peliculas favoritas del usuario
	directors = stalked_user['profile'].directors.all()

	#directors = Director.objects.filter(user_name=username) # .Title.objects.all()
	movies = Title.objects.filter(user_name=stalked_user['name']).order_by('-rating')[:3]

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


def get_movies_by_age(request):
	# Remove the last letter 's' from the year so it can be used as a number.
	age_1 = int(request.GET['value'][:-1])
	age_2 = str(age_1 + 9)
	movies_from_age = Title.objects.all().filter(year__range=[age_1, age_2])
	movies_dict = {}
	movies_list = []
	k = 0

	for i in movies_from_age:
		movies_list.append({})
		movies_list[k]["director"] = i.director.director_name
		movies_list[k]["movie_name"] = str(i.movie_name)
		movies_list[k]["slug"] = str(i.slug)
		movies_list[k]["year"] = str(i.year)
		movies_list[k]["rating"] = str(i.rating)
		movies_list[k]["poster"] = str(i.poster)
		k += 1
	print 'movies_list ', movies_list
	las_movies = json.dumps(movies_list)
	print "WWWWWWWWWW ", las_movies
	print 'movies_from_age ', movies_from_age

	# This is AJAX
	return HttpResponse(las_movies)

# exitos
def get_movies_by_rating(request):
	titles = Title.objects.all().order_by('-rating')[:20]

	list_with_movie_name = []
	unique_set = []
	my_list = []

	for i in range(len(titles)):
		list_with_movie_name.append([titles[i], titles[i].movie_name])

	for i in range(len(list_with_movie_name)):
		if list_with_movie_name[i][1] not in unique_set:
			my_list.append(list_with_movie_name[i][0])
			unique_set.append(list_with_movie_name[i][1])

	return render(request, 'califas/exitos.html', {'titles': my_list})


def title_detail(request, movie_name_slug):
	pass