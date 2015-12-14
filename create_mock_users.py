#--<coding:utf8-->
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinesnob.settings')

import django

django.setup()

from django.contrib.auth.models import User
from califas.models import UserProfile, Director, Title, Review, Friend

from unidecode import unidecode
import random

def populate():

	reviews = [
		u"Pésima, exijo que me devuelvan mi dinero.",
		u"Me dormí apenas empezaba; a mis niños les encantó.",
		u"Es una buena película, con momentos interesantes.",
		u"De una belleza que estremece. Emociones que llegan al alma.",
		u"La mejor película desde el Padrino, con unos personajes entrañables."
	]

	users_image_path = 'profile_images/'
	movies_image_path = 'movie_images/'
	directors_image_path = 'director_images/'

	users = [
		{'username': 'andrebazin', 'email': 'andre@bazin.com', 'password': 'andrebazin',
		     'name': u'André Bazin', 'about': u'Cahiers du Cinema, le mellieur du monde!', 'avatar': users_image_path+'andre_bazin-w.jpg'},

		{'username': 'rogerebert', 'email': 'roger@ebert.com', 'password': 'rogerebert',
		     'name': u'Roger Ebert', 'about': u'I give all movies two thumbs up!', 'avatar': users_image_path+'roger_ebert-w.jpg'},

		{'username': 'dilyspowell', 'email': 'dilys@powell.com', 'password': 'dilyspowell',
		     'name': u'Dilys Powell', 'about': u'I love wearing a Santa Claus hat when Summer\'s high', 'avatar': users_image_path+'dilys_powell-w.jpg'},

		{'username': 'jonathanrosenbaum', 'email': 'jonathan@rosenbaum.com', 'password': 'jonathanrosenbaum', 'name': u'Jonathan Rosenbaum', 'about': u'Lovin\' Indies all the way!', 'avatar': users_image_path+'jonathan_rosenbaum-w.jpg'},

		{'username': 'paulinekael', 'email': 'pauline@kael.com', 'password': 'paulinekael', 'name': u'Pauline Kael', 'about': u'Watching movies on the sofa with pizza, that\'s what life is all about. Happiness, bliss.', 'avatar': users_image_path+'pauline_kael-w.jpg'},
	]

	print "Setting up users..."
	user_and_profile = []
	for x in users:
		user = User.objects.create_user(username=x['username'], email=x['email'], password=x['password'])
		user.save()
		user_profile = UserProfile(usr=user, username=x['username'], name=x['name'], email=x['email'],about=x['about'], avatar=x['avatar'])
		user_profile.save()
		user_and_profile.append({'user': user, 'profile': user_profile})

	# Directors
	print "Setting up directors..."
	truffaut = Director(nationality=u'Francia', name=u'Francois Truffaut', about=u'El mejor director de Francia.', birth=1932, death=1984, picture=directors_image_path+'truffaut-w.jpg')
	truffaut.save()

	kubrick = Director(nationality=u'Estados Unidos', name=u'Stanley Kubrick', about=u'Director de cine, guionista, productor y fotógrafo estadounidense. Considerado por muchos como uno de los cineastas más influyentes del siglo XX.', birth=1928, death=1999, picture=directors_image_path+'kubrick-w.jpg')
	kubrick.save()

	herzog = Director(nationality=u'Alemania', name=u'Werner Herzog', about=u'Hacia los 17 años decidió dedicarse al cine. Para pagarse sus películas, trabajó en diversos oficios, que combinaba con sus estudios secundarios y más tarde universitarios.', birth=1942, death=0, picture=directors_image_path+'herzog-w.jpg')
	herzog.save()

	inarritu = Director(nationality=u'México', name=u'Alejandro González Iñárritu', about='Cruzando el Atlántico y laborando en un barco carguero, primero a los 17 y después a los 19 años, González Iñárritu trabajó en Europa y África en dos diferentes periodos de su vida.', birth=1963, death=0, picture=directors_image_path+'inarritu-w.jpg')
	inarritu.save()

	lynch = Director(nationality=u'Estados Unidos', name=u'David Lynch', about=u'Reconocido admirador de Jacques Tati, Ingmar Bergman o Werner Herzog, su amor por el dadaísmo y el surrealismo queda patente en algunas de sus películas, cuya misteriosa atmósfera mezcla lo cotidiano con lo soñado, escapando a veces a la comprensión exhaustiva del espectador.', birth=1946, death=0, picture=directors_image_path+'lynch-w.jpg')
	lynch.save()

	tornatore = Director(nationality=u'Italia', name=u'Giuseppe Tornatore', about=u'Se aficionó a la fotografía desde muy niño. Más tarde, después de poner en escena, con tan sólo dieciséis años, textos de Luigi Pirandello y Eduardo De Filippo, se acercó al cine rodando documentales de gran valor artístico.', birth=1956, death=0, picture=directors_image_path+'tornatore-w.jpg')
	tornatore.save()

	trier = Director(nationality=u'Dinamarca', name=u'Lars Von Trier', about=u'Junto a Thomas Vinterberg estableció las reglas del manifiesto Dogma 95. Destaca ante todo por su fuerte personalidad creativa y es considerado uno de los directores más innovadores y multidisciplinares del cine actual.', birth=1956, death=0, picture=directors_image_path+'trier-w.jpg')
	trier.save()

	gondry = Director(nationality=u'Francia', name=u'Michel Gondry', about=u'El estilo de sus vídeos llamó la atención de la cantante Björk, quien le pidió dirigir el vídeo para su canción Human Behavior.', birth=1963, death=0, picture=directors_image_path+'gondry-w.jpg')
	gondry.save()

	dormael = Director(nationality=u'Bélgica', name=u'Jaco Van Dormael', about=u'Sus complejas películas, aclamadas por la crítica, se destacan especialmente por su representación respetuosa y comprensiva de las personas con discapacidad tanto mental como física.', birth=1957, death=0, picture=directors_image_path+'dormael-w.jpg')
	dormael.save()

	kassovitz = Director(nationality=u'Francia', name=u'Mathieu Kassovitz', about=u'Después del éxito de su primer largometraje Métisse (1993), adquirió notoriedad con El odio (La Haine, 1995), película que escribió y realizó y con la que alcanzó éxito internacional.', birth=1967, death=0, picture=directors_image_path+'kassovitz-w.jpg')
	kassovitz.save()

	jackson = Director(nationality=u'Nueva Zelanda', name=u'Peter Jackson', about=u'Conocido especialmente por dirigir, producir y coescribir1 la trilogía cinematográfica de El Señor de los Anillos: La Comunidad del Anillo (2001), Las dos torres (2002) y El retorno del Rey (2003).', birth=1961, death=0, picture=directors_image_path+'jackson-w.jpg')
	jackson.save()

	hitchcock = Director(nationality=u'Reino Unido', name=u'Alfred Hitchcock', about=u'Fue pionero en muchas de las técnicas que caracterizan a los géneros cinematográficos del suspense y el thriller psicológico. Las películas de Hitchcock también abordan a menudo temas del psicoanálisis y tienen marcadas connotaciones sexuales.', birth=1899, death=1980, picture=directors_image_path+'hitchcock-w.jpg')
	hitchcock.save()

	tarantino = Director(nationality=u'Estados Unidos', name=u'Quentin Tarantino', about=u'Sus películas se caracterizan en general por emplear historias no lineales, la estetización de la violencia, las influencias estilísticas del Grindhouse, el kung fu y los spaghetti western.', birth=1963, death=0, picture=directors_image_path+'tarantino-w.jpg')
	tarantino.save()

	scorsese = Director(nationality=u'Estados Unidos', name=u'Martin Scorsese', about=u'Inicialmente, Scorsese planeaba ordenarse como sacerdote, lo que se nota en muchas de sus películas, que reflejan una crianza católica. Sus obras abordan principalmente los temas de la vida italo-estadounidense.', birth=1942, death=0, picture=directors_image_path+'scorsese-w.jpg')
	scorsese.save()

	directors_list = [scorsese, tarantino, hitchcock, jackson, kassovitz, dormael, gondry, trier, tornatore, lynch, inarritu, herzog, kubrick, truffaut]

	movies = [
		{'name': u'Les 400 coups', 'year': 1959, 'director': truffaut, 'genre': u'drama', 'poster': movies_image_path+'400_coups-w.jpg'},
		{'name': '2001', 'year': 1968, 'director': kubrick, 'genre': u'ciencia ficción/épico', 'poster': movies_image_path+'2001-w.jpg'},
		{'name': u'Aguirre der Zorn Gottes', 'year': 1972, 'director': herzog, 'genre': u'drama', 'poster': movies_image_path+'aguirre-w.jpg'},
		{'name': u'Amores Perros', 'year': 1995, 'director': inarritu, 'genre': u'drama', 'poster': movies_image_path+'amores_perros-w.jpg'},
		{'name': u'Birdman', 'year': 2014, 'director': inarritu, 'genre': u'drama/comedia', 'poster': movies_image_path+'birdman-w.jpg'},
		{'name': u'Blue Velvet', 'year': 1986, 'director': lynch, 'genre': u'drama/terror', 'poster': movies_image_path+'blue_velvet-w.jpg'},
		{'name': u'Cinema Paradiso', 'year': 1988, 'director': tornatore, 'genre': u'drama', 'poster': movies_image_path+'cinema_paradiso-w.jpg'},
		{'name': u'Dogville', 'year': 2003, 'director': trier, 'genre': u'drama', 'poster': movies_image_path+'dogville-w.jpg'},
		{'name': u'Eternal Sunshine of the Spotless Mind', 'year': 2004, 'director': gondry, 'genre': u'drama', 'poster': movies_image_path+'eternal_sunshine-w.jpg'},
		{'name': u'Le Huitieme Jour', 'year': 1996, 'director': dormael, 'genre': u'drama/comedia', 'poster': movies_image_path+'huitieme_jour-w.jpg'},
		{'name': u'La Haine', 'year': 1995, 'director': kassovitz, 'genre': u'drama', 'poster': movies_image_path+'la_haine-w.jpg'},
		{'name': u'The Lord of the Rings', 'year': 2001, 'director': jackson, 'genre': u'épico', 'poster': movies_image_path+'lord_of_the_rings-w.jpg'},
		{'name': u'Psycho', 'year': 2001, 'director': hitchcock, 'genre': u'terror/suspenso', 'poster': movies_image_path+'psycho-w.jpg'},
		{'name': u'Pulp Fiction', 'year': 1994, 'director': tarantino, 'genre': u'drama/comedia', 'poster': movies_image_path+'pulp_fiction-w.jpg'},
		{'name': u'Taxi Driver', 'year': 1976, 'director': scorsese, 'genre': u'drama', 'poster': movies_image_path+'taxi_driver-w.jpg'},
	]

	print "Setting up reviews..."
	for z in movies:
		random_users = random.randint(1, 3)
		tit = Title(name=z['name'], year=z['year'], director=z['director'])
		tit.save()
		for i in range(random_users):
			users = [0, 1, 2, 3, 4]
			random_rating = random.randint(0, 4)
			current_user = random.choice(users)
			print current_user
			tit.users.add(user_and_profile[current_user]['profile'])
			z['director'].users.add(user_and_profile[current_user]['profile']) # is this necessary?
			user_and_profile[current_user]['profile'].directors.add(tit.director)

			rev = Review(genre=z['genre'], review=reviews[random_rating], rating=random_rating+1, poster=z['poster'], user=user_and_profile[current_user]['profile'], title=tit)
			rev.save()
			users.pop(current_user)

	print "Done!"

if __name__ == '__main__':
	populate()