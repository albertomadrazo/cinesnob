#--<encoding:utf8>--
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext
from califas.models import Director, Title
from califas.forms import TitleForm, DirectorForm, UserForm, UserProfileForm
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# from califas import funciones

def index(request):
	context = RequestContext(request)
	directors_list = Director.objects.all() # funciones.call_directors()
	#directors_list = Director.objects.all()
	context_dict = {'directors_list': directors_list}
	#for director in directors_list:
	#	print "===========", director.slug

	#for director in directors_list:
	#	director.url = director.director_name.replace(' ', '_')

	# render the response and return to the client.
	return render(request, 'califas/index.html', context_dict)
	#return render_to_response('califas/index.html', context_dict, context)

def base(request):
	context = RequestContext(request)
	context_dict ={'uno':1}
	return render_to_response('califas/base.html', context_dict, context)

def director(request, director_name_slug): # request is a mandatory argument
	print "DIRECTOR.VIEW"

	context = RequestContext(request)
	#director_name = director_name_url.replace('_', ' ')
	#context_dict = {'director_name': director_name}
	context_dict ={}

	try:
		director = Director.objects.get(slug=director_name_slug)
		titles = Title.objects.filter(director=director)
		context_dict['titles'] = titles
		context_dict['director_name'] = director
		context_dict['director_name_slug'] = director_name_slug
	except Director.DoesNotExist:
		pass

	for titulo in titles:
		titulo.url = titulo.movie_name.replace(' ', '_')

	return render_to_response('califas/director.html', context_dict, context)

@login_required
def nueva(request):
	print "NUEVA.VIEW"
	# Get the context from the request
	context = RequestContext(request)

	# A HTTP POST?
	if request.method == 'POST':
		#print request.POST[u'ratos']

		director_name = request.POST[u'director_nameko']
		title_form = TitleForm(request.POST)

#		# have we been provided with a valid form?
		if title_form.is_valid():
			nuevo_titulo = title_form.save(commit=False)#

			try:
				director = Director.objects.get(director_name=director_name)
				nuevo_titulo.director = director
			except Director.DoesNotExist:
				director = Director.objects.get_or_create(director_name=director_name) # o DirectorForm?
				director = Director.objects.get(director_name=director_name)				
				nuevo_titulo.director = director

			nuevo_titulo.save()
#			# Now call the index() view.
#			# The user will be shown the homepage.
#			return index(request)
		else:
#			# The supplied form contains errors - just print them to the terminal
			print title_form.errors

		directors_list = Director.objects.all() #funciones.call_directors()
		#url = HttpResponseRedirect(reverse('view.index'))
		#return render_to_response('califas/', directors_list, context) #HttpResponseRedirect('/califas/index.html')
		return render_to_response('califas/index.html', {'directors_list':directors_list}, context)

	else:
		# If the supplied request was not a post, display the form.
		title_form = TitleForm()
	# Bad form (or no details), no form supplied...
	# Render the form with error messages(if any).
		
		return render_to_response('califas/nueva.html', {'title_form': title_form}, context)

# en esta view, vamos a dar el detalle de la pelicula seleccionada
def pelicula(request, director_name_slug, movie_name_slug):
	print "PELICULA.VIEW"
	context = RequestContext(request)
	#movie_name = movie_name_detail.replace('_', ' ')
	#director_name = director_name_url.replace('_', ' ')
	context_dict = {'director_name': director_name_slug}
	try:
		director = Director.objects.get(slug=director_name_slug)
		titles = Title.objects.filter(slug=movie_name_slug)
		context_dict['titles'] = titles
		context_dict['director_name'] = director
	except Director.DoesNotExist:
		pass

	the_url = 'califas/pelicula.html'
	the_url = the_url.replace(' ', '')
	return render_to_response(the_url, context_dict, context)

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

def lista_usuarios(request):
	usuarios = User.objects.all()
	for user in usuarios:
		print user.username

	context_dict = {'usuarios': usuarios }

	return render(request, 'califas/usuarios.html', context_dict)