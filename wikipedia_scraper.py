#Run script every 3 hours
#Possible issues - score is updated without try scorers

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

team_names = []
teams = Team.objects.all()
for team in teams:
	team_names.append(team.team_name)

database_player_names = []
database_players = Player.objects.all()
for pl in database_players:
	database_player_names.append(pl.name)


class TryClass:

	player_name = ""
	minute = 0
	team_name = ""


def make_soup(url):

	thepage = urllib.request.urlopen(url)
	soupdata = BeautifulSoup(thepage, "html.parser")
	return soupdata


def scrape_wiki(game_number):

	event_block = soup.findAll('div', {'class': 'vevent summary'})[game_number]

	#Data and Time
	dateAndTime = event_block.find('tbody').get_text(
		strip=True, separator=',').split(',')
	try:
		date = dateAndTime[0]
		time = dateAndTime[1]

	except:
		print("Date error")

	d = datetime.strptime(date, '%d %B %Y')
	dateTimeFormat = d.strftime('%Y-%m-%d')

	# Teams - matches with database
	teams = event_block.findAll('th', {'class': 'vcard'})
	homeTeam = difflib.get_close_matches(
		teams[0].text.replace("(1 BP)", "").strip(), team_names)[0]
	awayTeam = difflib.get_close_matches(
		teams[1].text.replace("(1 BP)", "").strip(), team_names)[0]
	homeTeamObj = Team.objects.filter(team_name=homeTeam)[0]
	awayTeamObj = Team.objects.filter(team_name=awayTeam)[0]

	# Scores
	score = event_block.findAll('th')[1].text.strip()
	if "v" in score:
		# Game has not been completed
		return False

	homeScore = score.split('–')[0]
	awayScore = score.split('–')[1]

	try:
	# Match
		if len(Match.objects.filter(date=dateTimeFormat, home_team=homeTeamObj, away_team=awayTeamObj, home_score=homeScore, away_score=awayScore)) == 0:
			match = Match(date=dateTimeFormat, home_team=homeTeamObj,
						  away_team=awayTeamObj, home_score=homeScore, away_score=awayScore)
			
			print("New match created: " + str(Match))
			match.save()
		else:
			match = Match.objects.filter(date=dateTimeFormat, home_team=homeTeamObj,
										 away_team=awayTeamObj, home_score=homeScore, away_score=awayScore)[0]

	except:
		return

	if match.tries_created == 1:
		return True

	tries = []
	processing_hometeam = True

	for t in event_block.findAll('td'):

		if "Try:" in t.text:
			scorers_list = t.get_text(strip=True, separator=',').split(',')
			try_scorers = t.findAll('a')
			try_scorer_names = []

			for try_scorer in try_scorers:
				try_scorer_names.append(try_scorer['title'].replace(
					'(page does not exist)', '').strip())

			try_scorer_name_itterator = 0
			current_try_scorer = ""

			for scorer in scorers_list:
				if scorer == 'Con:' or scorer == 'Pen:':
					break
				if scorer == 'Try:' or scorer == "c":
					continue

				if scorer[0].isalpha():
					try:
						current_try_scorer = try_scorer_names[try_scorer_name_itterator]
					except:
						break
					try_scorer_name_itterator += 1
					continue

				split_times_from_brackets = scorer.split(" ")

				for split_time in split_times_from_brackets:
					if "'" in split_time:
						try:
							single_try = TryClass()
							single_try.player_name = current_try_scorer.replace(
								"(rugby union)", "").replace("(rugby player)", "").strip()
							single_try.minute = int(
								re.findall("\d+", split_time)[0])

							if processing_hometeam:
								single_try.team_name = homeTeam
							else:
								single_try.team_name = awayTeam
							tries.append(single_try)
						except:
							continue
			processing_hometeam = False

	tries_in_wikipedia = False

	for trie in tries:

		if len(difflib.get_close_matches(trie.player_name.strip(), database_player_names)) == 0:
			# Add Player
			player_team = Team.objects.filter(team_name=trie.team_name)[0]
			player = Player(name=trie.player_name, team=player_team,
							age=0, picture="hi", coolfact='hi')
			player.save()
			print("New player created: " + str(trie.player_name))
		else:
			try:
				player = Player.objects.filter(name=trie.player_name)[0]
			except:
				continue

		database_try = Try(match=match, player=player, minute=trie.minute)
		tries_in_wikipedia = True
		#database_try.save()

	if tries_in_wikipedia:
		match.tries_created = 1
		match.save()

	return True

urls = ["https://en.wikipedia.org/wiki/2019_Rugby_World_Cup_Pool_A","https://en.wikipedia.org/wiki/2019_Rugby_World_Cup_Pool_B","https://en.wikipedia.org/wiki/2019_Rugby_World_Cup_Pool_C","https://en.wikipedia.org/wiki/2019_Rugby_World_Cup_Pool_D","https://en.wikipedia.org/wiki/2018%E2%80%9319_Premiership_Rugby","https://en.wikipedia.org/wiki/2019_Rugby_World_Cup_warm-up_matches","https://en.wikipedia.org/wiki/2015_Rugby_World_Cup","https://en.wikipedia.org/wiki/2019_Six_Nations_Championship"]
for url in urls:
	soup = make_soup(url)

	for game_number in range(0, 1000):
		try:
			if not scrape_wiki(game_number):
				break
		except IndexError:
			break
