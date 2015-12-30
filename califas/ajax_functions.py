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

import views

def get_movies_by_age(request):
	# Remove the last letter 's' from the year and convert to integer.
	age_1 = int(request.GET['value'][:-1])
	# add a range of 9 years so it completes the decade, ex. 199 8
	age_2 = str(age_1 + 9)

	movie_filter = Title.objects.filter(year__range=[age_1, age_2])
	movies_from_age = views.get_movies(movie_filter, 20)
	
	movies_dict = {}
	movies_list = []

	for k, i in enumerate(movies_from_age):
		movies_list.append({})
		movies_list[k]["director"] = str(i['director'])
		movies_list[k]["movie_name"] = str(i['name'])
		movies_list[k]["slug"] = str(i['slug'])
		movies_list[k]["genre"] = i['genre']#[0]
		movies_list[k]["year"] = str(i['year'])
		movies_list[k]["rating"] = i['rating']
		movies_list[k]["opinion"] = i['opinion']#random.choice(i['opinion'])
		movies_list[k]["poster"] = str(i['poster'])

	las_movies = json.dumps(movies_list)

	# This is AJAX
	return HttpResponse(las_movies)


@login_required
def delete_title(request, title_slug):
	user = get_user_and_profile()['profile']
	Title.objects.get(slug=title_slug, users=user)
	print 'title_to_delete > ', title_to_delete

	return HttpResponse("OK")