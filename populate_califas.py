import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinesnob.settings')

import django
django.setup()

from califas.models import Director, Title


def populate():
	gen_review = "Great movie! I was shocked!",

	hitchcock = add_director('Alfred Hitchcock')
	add_title(director=hitchcock,
		movie_name="Psycho",
		year="1956",
		genre="Suspense",
		review=gen_review,
		rating=5,
	)

	add_title(director=hitchcock,
		movie_name="Rear Window",
		year=1963,
		genre="Suspense",
		review=gen_review,
		rating=5,
		)

	truffaut = add_director('Francois Truffaut')
	add_title(director=truffaut,
		movie_name="400 Coups",
		year=1959,
		genre="Drama",
		review="Masterpiece",
		rating=5,
		)

	add_title(director=truffaut,
		movie_name="La Nuit Americaine",
		year=1976,
		genre="Comedy",
		review=gen_review,
		rating=5,
		)

	einsenstein = add_director('Sergey Einsenstein')
	add_title(director=einsenstein,
		movie_name="Octubre",
		year=1927,
		genre="historico-propagandistico",
		review=gen_review,
		rating=5,
		)
	add_title(director=einsenstein,
		movie_name="El Acorazado Potemkin",
		year=1924,
		genre="drama",
		review="mnhe nravitza!",
		rating=5,
		)

	# Print out.
	for c in Director.objects.all():
		for p in Title.objects.filter(director=c):
			print "- {0} - {1}".format(str(c), str(p))

def add_title(director, movie_name, year, genre, review, rating):
	t = Title.objects.get_or_create(director=director, 
									movie_name=movie_name,
									year=year,
									genre=genre,
									review=review,
									rating=rating	
									)
	return t

def add_director(director_name):
	c = Director.objects.get_or_create(director_name=director_name)[0]
	return c

# start execution
if __name__ == '__main__':
	print "Starting Califas Population Script..."
	populate()
