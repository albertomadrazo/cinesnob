from general_imports import *
from generic_functions import *
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
def delete_title(request):
	print "***********************"
	print request
	print "***********************"
	to_del = request.POST['value']
	print "to_del = ", to_del
	print type(request.user)
	print 'request.user =============================', str(request.user)
	current_user = UserProfile.objects.get(username=str(request.user))
	# user = get_user_and_profile(request.user)['profile']
	print "current_user =", current_user
	print type(current_user)
	title_to_delete = Title.objects.filter(users=current_user, name=to_del)
	print 'title_to_delete > ', title_to_delete
	title_to_delete.delete()
	return HttpResponse("OK")