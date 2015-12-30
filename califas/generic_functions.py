from general_imports import *


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
