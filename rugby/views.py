from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.views.generic import TemplateView, DetailView
from.models import Player
from.models import Team
from.models import Match
from.models import Try
from.models import League
#from .filters import TryFilter
from .forms import SubmitUrlForm
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Q

class templateInfo:
	player_name = ""
	player_pic = ""
	player_link = ""
	player_team = ""
	player_team_link = ""
	try_url = ""
	try_match = ""
	match_link = ""

class matchInfo:
	video_link = ""
	name = ""
	match_link = ""



def search(request):
	try_list = Try.objects.all()
	try_filter = TryFilter(request.GET, queryset=try_list)

	return render(request, 'rugby/test.html', {'filter':try_filter})


class TryFormView(generic.ListView):
	
	template_name = "rugby/try_form.html"

	def get_queryset(self):
		single_match = Match.objects.filter(tries_created=0).order_by("-date").first()
		match_players = []
		match_players.append(single_match)
		home_players = Player.objects.all().filter(team=single_match.home_team)

		for home_player in home_players:
			match_players.append(home_player)

		away_players = Player.objects.all().filter(team=single_match.away_team)

		for away_player in away_players:
			match_players.append(away_player)

		return match_players

	@method_decorator(csrf_exempt)
	def post(self, request, *args, **kwargs):
		names = request.POST.getlist('player_name')
		starts = request.POST.getlist('start_time')
		ends = request.POST.getlist('end_time')

		print(names)
		game = Match.objects.filter(tries_created=0).order_by("-date")[0]



		for n,s,e in zip(names,starts,ends):

			if n == 'Select Player':
				continue

			fixed_video_link = game.video_link + "?start=" + str(s) + "&end=" + str(e)

			p = Try(match=game,player=Player.objects.filter(name=n).first(),video_link=fixed_video_link,viewcount=0,ratings_average=0,start_time=s,end_time=e)
			p.save()


		game.tries_created = 1
		game.save()


		return render(request, "rugby/thankyou.html", {})

class TryProcessingView(generic.ListView):
	template_name = "rugby/tryprocessing.html"

	def get_queryset(self):
		my_context = {
			"match": [],
			"tries": [],
			"video_link":[],
			"players":[]
		}

		#Get the latest match
		latest_match = Match.objects.filter(video_downloaded=True).order_by('date')[:10][0]
		my_context["match"] = latest_match

		#Get tries from latest matches
		tries = Try.objects.filter(match=latest_match)
		my_context["tries"] = tries

		my_context["players"] = Player.objects.all()

		my_context["video_link"] = "https://www.youtube.com/embed/" + latest_match.video_link.split("=")[1] + "?rel=0"

		return my_context

	def post(self, request, *args, **kwargs):
		pass


class AllPlayersView(generic.ListView):
	template_name = "rugby/allplayers.html"

	def get_queryset(self):
		return Player.objects.all()

class DetailPlayerView(generic.DetailView):

	model = Player
	template_name = "rugby/playerdetails.html"


@method_decorator(csrf_exempt, name='dispatch')
class TeamView(DetailView):
	model = Team

	def get_context_data(self, **kwargs):

		#Get Player
		context = super(TeamView, self).get_context_data(**kwargs)
		individual_team = context["object"]

		#Retrieve tries
		my_context = {
			"tries": [],
		}

		my_context["tries"] = prepareTryData(team_request=individual_team)
		my_context["matches"] = prepareMatchData(team_request=individual_team)

		#Send to template
		return my_context

	def post(self, request, *args, **kwargs):

		
		video_link = request.POST.getlist('video_link')[0]
		print(video_link)
		
		try_object = Try.objects.filter(video_link=video_link)[0]
		player_object = try_object.player
		match_object = try_object.match

		if try_object.team.team_name == match_object.home_team.team_name:
			try_object.team = match_object.away_team
			player_object.internation_team = match_object.away_team
		else:
			try_object.team = match_object.home_team
			player_object.internation_team = match_object.home_team

		try_object.save()
		player_object.save()

		return HttpResponse('success')





class MatchView(DetailView):
	model = Match

	def get_context_data(self, **kwargs):

		#Get Player
		context = super(MatchView, self).get_context_data(**kwargs)
		individual_match = context["object"]

		#Retrieve tries
		my_context = {
			"tries": [],
			"matches":[]
		}


		my_context["tries"] = prepareTryData(match_request=individual_match)
		my_context["matches"] = prepareMatchData(match_request=individual_match)

		#Send to template
		return my_context

class LeagueView(DetailView):
	model = League

	def get_context_data(self, **kwargs):

		#Get Player
		context = super(LeagueView, self).get_context_data(**kwargs)
		individual_league = context["object"]

		#Retrieve tries
		my_context = {
			"tries": [],
			"matches":[]
		}

	
		my_context["tries"] = prepareTryData(league_request=individual_league)
		my_context["matches"] = prepareMatchData(league_request=individual_league)

		#Send to template
		return my_context


class PlayerView(DetailView):
	model = Player

	def get_context_data(self, **kwargs):

		#Get Player
		context = super(PlayerView, self).get_context_data(**kwargs)
		individual_player = context["object"]

		#Retrieve tries
		my_context = {
			"tries": [],
		}

		my_context["tries"] = prepareTryData(player_request=individual_player)

		#Send to template
		return my_context


def index(request):

	#Retrieve tries
	my_context = {
		"tries": [],
		"matches": []
	}

	my_context["tries"] = prepareTryData()
	my_context["matches"] = prepareMatchData()

	#Send to template
	return render(request, 'rugby/home.html',my_context)

@csrf_exempt
def tryprocessing(request):

	my_context = {
		"match": [],
		"tries": [],
		"video_link":[],
		"players":[],
		"amount":[]
	}

	all_matches = Match.objects.all()

	my_context["amount"] = len(Match.objects.filter(video_link_found=1,match_completely_processed=0,error=0,date__year='2019'))

	tries = Try.objects.all()
	for t in tries:
		if "streamable" in t.video_link:
			t.delete()
	

	for m in all_matches:
		if "youtube" not in m.video_link:
			m.delete()

	superleague = League.objects.filter(name="International")[0]

	for m in Match.objects.filter(video_link_found=1,match_completely_processed=0,error=0,date__year='2019',league_id=superleague).order_by('-date'):
		print(m)

	#Get the latest match
	latest_match = Match.objects.filter(video_link_found=1,match_completely_processed=0,error=0,date__year='2019',league_id=superleague).order_by('-date')[0]
	my_context["match"] = latest_match
	
	if request.method =="POST":

		if "finished" in request.POST:
			latest_match.match_completely_processed = 1
			latest_match.save()
		elif "error" in request.POST:
			latest_match.error = 1
			latest_match.save()
		else:
	
			player_name = request.POST['player_name']
			start_time_minute = request.POST['start_time_minute']
			start_time_second = request.POST['start_time_second']
			end_time_minute = request.POST['end_time_minute']
			end_time_second = request.POST['end_time_second']
			team_id = int(request.POST['team_id'])

			start_time = minutes_and_seconds_to_seconds(int(start_time_minute),int(start_time_second))
			end_time = minutes_and_seconds_to_seconds(int(end_time_minute),int(end_time_second))

			new_link = add_times_to_video_link(latest_match.video_link,start_time,end_time)

			print("#" + player_name + "#")

			try_scorer_object = Player.objects.filter(name=player_name)[0]
			team_from_id = Team.objects.filter(id=team_id)[0]

			try_object = Try(match=latest_match,player=try_scorer_object,video_link=new_link,start_time=start_time,end_time=end_time,team=team_from_id)
			
			if int(team_id) < 63 and int(team_id) > 44:
				try_scorer_object.internation_team = team_from_id
				try_scorer_object.save()

			try_object.save()

			
			return HttpResponse('success') # if everything

		return render(request, 'rugby/tryprocessing.html', {})

	else:

		my_context["players"] = Player.objects.all()

		if "embed" not in latest_match.video_link:
			print(latest_match.video_link)
			my_context["video_link"] = "https://www.youtube.com/embed/" + latest_match.video_link.split("=")[1] + "?rel=0"
		else:
			my_context["video_link"] = latest_match.video_link + "?rel=0"

		print(my_context["video_link"])
		return render(request, 'rugby/tryprocessing.html', my_context)

def contact(request):
	return render(request, 'rugby/basic.html', {'content':['Please email maidenrhys@gmail.com']})

def prepareTryData(player_request=None, match_request=None, team_request=None, league_request=None):

	try_query = None

	if player_request is not None:
		try_query = Try.objects.filter(player=player_request).order_by('-match__date')[:20]
	elif match_request is not None:
		try_query = Try.objects.filter(match=match_request).order_by('-match__date')[:20]
	elif team_request is not None:
		try_query = Try.objects.filter(team=team_request).order_by('-match__date')[:50]
	elif league_request is not None:
		print(league_request)
		try_query = Try.objects.filter(match__league_id=league_request).order_by('-match__date')[:50]
	else:
		try_query = Try.objects.all().order_by('-match__date')[:8]

	tries_for_template = []


	for t in try_query:

		tryBlock = templateInfo()
		tryBlock.player_name = t.player.name
		tryBlock.player_pic = t.player.picture
		
		tryBlock.player_link = "http://127.0.0.1:8000/player/" + str(t.player.id)
		tryBlock.player_team = t.player.team.team_name
		tryBlock.player_team_link = "http://127.0.0.1:8000/team/" + str(t.player.team.id)
		tryBlock.try_url = t.video_link
		tryBlock.try_match = t.match
		tryBlock.match_link = "http://127.0.0.1:8000/match/" + str(t.match.id)
		tryBlock.video_link = t.video_link

		tries_for_template.append(tryBlock)

	return tries_for_template

def prepareMatchData(player_request=None, match_request=None, team_request=None, league_request=None):

	matches = []

	if match_request is not None:
		matches.append(match_request)
	elif team_request is not None:
		print("HH")
		matches = Match.objects.filter(Q(home_team=team_request) | Q(away_team=team_request)).order_by('-date')[:12]
	elif league_request is not None:
		matches = Match.objects.filter(league_id=league_request).order_by('-date')[:12]
	else:
		matches = Match.objects.all().order_by('-date')[:8]

	
	matches_for_template = []

	print(len(matches))

	if len(matches) == 0:
		return matches_for_template

	for m in matches:
		matchBlock = matchInfo()
		matchBlock.video_link = youtube_to_embed(m.video_link)
		matchBlock.match_link = "http://127.0.0.1:8000/match/" + str(m.id)
		matchBlock.name = m
		matches_for_template.append(matchBlock)

	return matches_for_template

	
def minutes_and_seconds_to_seconds(minutes,seconds):
	
	seconds_from_minutes = minutes * 60
	return seconds + seconds_from_minutes

def add_times_to_video_link(video_link,start_time,end_time):
	link = "https://www.youtube.com/embed/" + video_link.split("=")[1] + "?start=" + str(start_time) + "&end=" + str(end_time) + ";rel=0"
	return link

def youtube_to_embed(original):
	print(original)

	if 'embed' in original:
		return original

	embedded = "https://www.youtube.com/embed/" + original.split("=")[1]
	return embedded









