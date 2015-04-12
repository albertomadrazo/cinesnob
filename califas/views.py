#--<encoding:utf8>--
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from califas.models import Director, Title, UserProfile, Friend
from califas.forms import TitleForm, DirectorForm, UserForm, UserProfileForm
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def get_user_or_profile(username):

	user_or_profile = {}
	user_name = User.objects.get(username=str(username))
	user_or_profile['name'] = user_name

	user = UserProfile.objects.all()
	for my_user in user:
		if my_user.user == user_name:
			user_or_profile['profile'] = my_user
			return user_or_profile

	return None


def index(request):

	current_user = str(request.user.username)
	context_dict = {}

	
	if current_user != '':
		
		the_user = get_user_or_profile(request.user)
		print the_user

		try:
			directors_list = the_user['profile'].directors.all() 
			context_dict = {'directors_list': directors_list}
			print "QQQQQQQQQQ", context_dict['directors_list']
		except:
			context_dict = {'directors_list': ''}

	recommendations = Title.objects.all().order_by('-rating')[:5]
	context_dict['recommendations'] = recommendations
	return render(request, 'califas/index.html', context_dict)


def base(request):

	context = RequestContext(request)
	context_dict ={'uno': 1}
	return render(request, 'califas/base.html', context_dict)

def director(request, director_name_slug): 
 
 	context_dict ={}
	user = get_user_or_profile(request.user)

	try:
		directors = user['profile'].directors.all()
		for direc in directors:
			if direc.slug == director_name_slug:
				director = direc

		titles = Title.objects.filter(
						director=director, user_name=user['name']).order_by('-year')
		context_dict['titles'] = titles
		context_dict['director_name'] = director
		context_dict['director_name_slug'] = director.director_name_slug
	except:
		print "You have no directors %s " % request.user

	return render(request, 'califas/director.html', context_dict)

@login_required
def nueva(request):

	if request.method == 'POST':
		director_found = False
		user = get_user_or_profile(request.user)

		director_name = request.POST[u'director_name']
		title_form = TitleForm(request.POST)

		# have we been provided with a valid form?
		if title_form.is_valid():
			nuevo_titulo = title_form.save(commit=False)
			nuevo_titulo.user_name = user['name']

			try:
				director = user['profile'].directors.get(director_name=director_name)
			except:
				director_list = Director.objects.all()

				for director in director_list:
					print director.director_name, director_name

					if director.director_name == director_name:
						director_found = True

					
				if director_found == False:	
					director = Director(director_name=director_name)
					
					director.save()
	
				user['profile'].directors.add(director)

			nuevo_titulo.director = director
			nuevo_titulo.save()
#			# Now call the index() view.
#			# The user will be shown the homepage.
#			return index(request)
		else:
#			# The supplied form contains errors - just print them to the terminal
			print title_form.errors

		directors_list = user['profile'].directors.all() #funciones.call_directors()
		#url = HttpResponseRedirect(reverse('view.index'))
		#return render_to_response('califas/', directors_list, context) #HttpResponseRedirect('/califas/index.html')
		return render(request, 'califas/index.html', {'directors_list':directors_list})

	else:
		# If the supplied request was not a post, display the form.
		title_form = TitleForm()
	# Bad form (or no details), no form supplied...
	# Render the form with error messages(if any).
		
		return render(request, 'califas/nueva.html', {'title_form': title_form})

# en esta view, vamos a dar el detalle de la pelicula seleccionada
def pelicula(request, director_name_slug, movie_name_slug):
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
	the_url = the_url.replace(' ', '')
	return render(request, the_url, context_dict)

def registrarse(request):
	registered = False

	if request.method == 'POST':
		# Va a haber dos formas en el registrarse.html
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
			befriend.is_friend = True
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

	user = get_user_or_profile(request.user)
	stalked_user = get_user_or_profile(username)
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


def befriend(request):

	usuario = str(request.GET[u'usuario'])
	amigarse = request.GET[u'amigarse']

	next_friend = Friend.objects.all()
	print "next_friend:" , next_friend
	for a in next_friend:
		if a.friend_name == amigarse:
			next_friend = a

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