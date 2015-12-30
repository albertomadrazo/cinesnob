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
