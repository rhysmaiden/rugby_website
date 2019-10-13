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
from rugby.views import AllPlayersView
from rugby.views import DetailPlayerView
from rugby.views import TeamView
from rugby.views import PlayerView
from rugby.views import TryFormView
from rugby.views import MatchView
from rugby.views import LeagueView
from datetime import date


urlpatterns = [
	url(r'^search/$', views.search, name='search'),
    #path('tryform/', TryFormView.as_view()),
    #url(r'^tryform/$', ListView.as_view(queryset=match_players, template_name="rugby/try_form.html")),
    url(r'^$', views.index, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^tryprocessing/$', views.tryprocessing, name='tryprocessing'),
    #url(r'^super/$', ListView.as_view(queryset=super_set, template_name="rugby/video_page.html")),
    #url(r'^aviva/$', ListView.as_view(queryset=aviva_set, template_name="rugby/video_page.html")),
    #url(r'^international/$', ListView.as_view(queryset=international_set, template_name="rugby/video_page.html")),
    #url(r'^pro/$', ListView.as_view(queryset=pro_set, template_name="rugby/video_page.html")),
    #url(r'^top/$', ListView.as_view(queryset=top_set, template_name="rugby/video_page.html")),
    #path('allplayers/', AllPlayersView.as_view()),
    url(r'^team/(?P<pk>[0-9]+)/$', TeamView.as_view(template_name="rugby/home.html")),
    url(r'^player/(?P<pk>[0-9]+)/$', PlayerView.as_view(template_name="rugby/home.html")),
    url(r'^match/(?P<pk>[0-9]+)/$', MatchView.as_view(template_name="rugby/home.html")),
    url(r'^league/(?P<pk>[0-9]+)/$', LeagueView.as_view(template_name="rugby/home.html")),
    #url(r'^(?P<pk>[0-9]+)/$', DetailView.as_view(model=Team, template_name="rugby/team_page.html")),
    #url(r'^(player?P<pk>\d+)$', DetailView.as_view(model=Player, template_name="rugby/video_page.html")),



    # All Teams #
    #url(r'^teams/crusaders$', ListView.as_view(queryset=super_set, template_name="rugby/video_page.html")),

]
