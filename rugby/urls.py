from django.conf.urls import url, include
from django.contrib import admin
from . import views
from django.views.generic import ListView, DetailView
from rugby.models import Match
from rugby.models import Try
from rugby.models import Player
from rugby.models import Team

import itertools
from itertools import chain
from django.urls import path
from rugby.views import TeamView
from rugby.views import PlayerView
from rugby.views import MatchView
from rugby.views import LeagueView



urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^tryprocessing/$', views.tryprocessing, name='tryprocessing'),
    url(r'^team/(?P<pk>[0-9]+)/$', TeamView.as_view(template_name="rugby/home.html")),
    url(r'^player/(?P<pk>[0-9]+)/$', PlayerView.as_view(template_name="rugby/home.html")),
    url(r'^match/(?P<pk>[0-9]+)/$', MatchView.as_view(template_name="rugby/home.html")),
    url(r'^league/(?P<pk>[0-9]+)/$', LeagueView.as_view(template_name="rugby/home.html")),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^ratings/', include('star_ratings.urls', namespace='ratings')),
]
