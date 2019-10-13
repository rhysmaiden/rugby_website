
import urllib
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime
import wikipedia
import os
import subprocess
import django
import re
import difflib

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rugby.settings")
django.setup()

from rugby.models import Match
from rugby.models import Team
from rugby.models import Player
from rugby.models import Try
from rugby.models import League

matches = Match.objects.all()

ints = ["New Zealand","Wales","England","Ireland","South Africa","Australia",
"France","Japan","Scotland","Argentina","Fiji","Italy","Georgia","Samoa",
"USA","Tonga","Spain","Uruguay","Romania","Canada","Namibia","Russia"]

prem = ["Worcester Warriors","Northampton Saints","Leicester Tigers","Saracens",
"Sale Sharks","Gloucester","Bath","London Irish","Newcastle Falcons","Harlequins","Wasps",
"Exeter Chiefs"]

pro_14 = ["Zebre","Benetton Treviso","Edinburgh","Glasgow Warriors","Cardiff Blues",
"Dragons","Ospreys","Scarlets","Connacht","Ulster","Munster","Leinster"]

teams = Team.objects.all()

for t in teams:
	if t.team_name in ints:
		t.league_id = League.objects.filter(name="International")[0]
	elif t.team_name in prem:
		t.league_id = League.objects.filter(name="Aviva Premiership")[0]
	elif t.team_name in prem:
		t.league_id = League.objects.filter(name="Pro 14")[0]

	t.save()



for m in matches:
	#print(m.home_team)
	m.league_id = m.home_team.league_id
	m.save()






# international_league = League.objects.filter(name="International")[0]

# matches = Match.objects.filter(match_completely_processed=1).order_by('-date')
# tries = Try.objects.all()



# for m in matches:
# 	try_found = False
# 	for t in tries:

# 		if t.match == m:
# 			try_found=True
# 			break
# 	if not try_found:
# 		m.match_completely_processed = 0
# 		m.save()

# for t in teams:
# 	if t.team_name in ints:
# 		t.league = "international"
# 		t.league_id = international_league
# 		t.save()



# for t in tries:
# 	if t.match.league == "international":
# 		if ints.index(t.match.home_team.team_name) < ints.index(t.match.away_team.team_name):
# 			t.team = t.match.home_team
# 			print(t.team)
# 		else:
# 			t.team = t.match.away_team
# 			print(t.team)
# 	else:
# 		t.team = t.player.team

# 	t.ratings_average = 0
# 	t.save()

# for trie in tries:
# 	if trie.team_id == 1:
# 		trie.team_id = 84
		#trie.save()
	#if trie.match.league == "international":
