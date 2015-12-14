import random
from django.template import Library
register = Library

@register.filter
def shuffle(arg):
	tmp = list(arg)[:]
	random.shuffle(tmp)

	return tmp