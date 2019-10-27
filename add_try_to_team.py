
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

team = Team.objects.filter(team_name="Australia")[0]

tries = Try.objects.filter(team=team,match__date__year='2019').order_by('-match__date')

table = "**" + "Tries by Australia in 2019" + "**\n"
table += "|Match|Player|Video Link|\n:--|:--|"

for t in tries:
    table += "\n|" + str(t.match) + "|" + t.player.name + "|" + t.video_link

print(table)
