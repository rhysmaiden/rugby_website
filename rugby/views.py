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

class searchBox:
    name = ""
    link = ''

@method_decorator(csrf_exempt, name='dispatch')
class TeamView(DetailView):
    model = Team

    def get_context_data(self, **kwargs):

        #Get Team
        context = super(TeamView, self).get_context_data(**kwargs)
        individual_team = context["object"]

        my_context = {
            "tries": [],
            "title":[],
            "players":[],
            "search_results":[],
            "try_count":[],
            "page":"",
            "logo":""
        }

        my_context["page"] = "Team"

        my_context["tries"] = prepareTryData(team_request=individual_team)
        my_context["matches"] = prepareMatchData(team_request=individual_team)
        my_context["title"] = individual_team.team_name

        my_context["players"] = Player.objects.filter(Q(team=individual_team) | Q(internation_team=individual_team))
        my_context["search_results"] = prepareSearchData()
        my_context["try_count"].append(str(len(Try.objects.all())))
        my_context["logo"] = individual_team.logo

        #Send to template
        return my_context

class MatchView(DetailView):
    model = Match

    def get_context_data(self, **kwargs):

        #Get Match
        context = super(MatchView, self).get_context_data(**kwargs)
        individual_match = context["object"]

        my_context = {
            "tries": [],
            "matches":[],
            "title":[],
            "search_results":[],
            "try_count":[],
            "page":""
        }

        my_context["tries"] = prepareTryData(match_request=individual_match)
        my_context["matches"] = prepareMatchData(match_request=individual_match)
        my_context["title"] = individual_match.home_team.team_name + " v " +  individual_match.away_team.team_name
        my_context["search_results"] = prepareSearchData()
        my_context["try_count"].append(len(Try.objects.all()))
        my_context["page"] = "Match"

        #Send to template
        return my_context

class LeagueView(DetailView):
    model = League

    def get_context_data(self, **kwargs):

        #Get League
        context = super(LeagueView, self).get_context_data(**kwargs)
        individual_league = context["object"]

        #Retrieve tries
        my_context = {
            "tries": [],
            "matches":[],
            "title":[],
            "search_results":[],
            "try_count":[],
            "page":""
        }

        my_context["tries"] = prepareTryData(league_request=individual_league)
        my_context["matches"] = prepareMatchData(league_request=individual_league)
        my_context["title"] = individual_league.name
        my_context["search_results"] = prepareSearchData()
        my_context["try_count"].append(len(Try.objects.all()))
        my_context["page"] = "League"

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
            "title":[],
            "search_results":[],
            "teams":[],
            "try_count":[],
            "page":""
        }

        my_context["try_count"].append(len(Try.objects.all()))
        my_context["tries"] = prepareTryData(player_request=individual_player)
        my_context["title"] = individual_player.name
        my_context["search_results"] = prepareSearchData()
        my_context["teams"].append(individual_player.team)
        my_context["teams"].append(individual_player.internation_team)
        my_context["page"] = "Player"

        #Send to template
        return my_context

def index(request):

    #Retrieve tries
    my_context = {
        "tries": [],
        "matches": [],
        "search_results":[],
        "try_count":[],
        "page":""
    }

    my_context["tries"] = prepareTryData()
    my_context["matches"] = prepareMatchData()
    my_context["search_results"] = prepareSearchData()
    my_context["try_count"].append(str(len(Try.objects.all())))
    my_context["page"] = "Home"

    #Send to template
    return render(request, 'rugby/home.html',my_context)

@csrf_exempt
def tryprocessing(request):

    my_context = {
        "match": [],
        "tries": [],
        "video_link":[],
        "players":[],
        "amount":[],
        "page":"",
        "try_count":""
    }

    my_context["amount"] = len(Match.objects.filter(video_link_found=1,match_completely_processed=0,error=0,date__year='2019'))
    my_context["try_count"] = len(Try.objects.all())

    tries = Try.objects.all()

    aviva_league = League.objects.filter(name="Aviva Premiership")[0]
    pro_league = League.objects.filter(name="Pro 14")[0]
    super_league = League.objects.filter(name="Super Rugby")[0]
    international_league = League.objects.filter(name="International")[0]

    #Get the latest match
    latest_match = Match.objects.filter(video_link_found=1,match_completely_processed=0,error=0).exclude(league_id=aviva_league).order_by('-date')[0]
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

            try_scorer_object = Player.objects.filter(name=player_name)[0]
            team_from_id = Team.objects.filter(id=team_id)[0]

            try_object = Try(match=latest_match,player=try_scorer_object,video_link=new_link,start_time=start_time,end_time=end_time,team=team_from_id)

            if int(team_id) < 63 and int(team_id) > 44:
                try_scorer_object.internation_team = team_from_id
                try_scorer_object.save()

            try_object.save()

            return HttpResponse('success')

        return render(request, 'rugby/tryprocessing.html', {})

    else:

        my_context["players"] = Player.objects.all()

        if "embed" not in latest_match.video_link:
            print(latest_match.video_link)
            my_context["video_link"] = "https://www.youtube.com/embed/" + latest_match.video_link.split("=")[1] + "?rel=0"
        else:
            my_context["video_link"] = latest_match.video_link + "?rel=0"

        return render(request, 'rugby/tryprocessing.html', my_context)

def contact(request):
    return render(request, 'rugby/basic.html', {'content':['Please email maidenrhys@gmail.com']})

def prepareTryData(player_request=None, match_request=None, team_request=None, league_request=None):

    try_query = None

    if player_request is not None:
        try_query = Try.objects.filter(player=player_request).order_by('-match__date')[:20]
    elif match_request is not None:
        matches = Match.objects.filter(home_team=match_request.home_team,away_team=match_request.away_team) | Match.objects.filter(home_team=match_request.away_team,away_team=match_request.home_team)
        try_query = Try.objects.filter(match__in=matches).order_by('-match__date')[:20]
    elif team_request is not None:
        try_query = Try.objects.filter(team=team_request).order_by('-match__date')[:50]
    elif league_request is not None:
        try_query = Try.objects.filter(match__league_id=league_request).order_by('-match__date')[:50]
    else:
        match_query = Match.objects.all().order_by('-date')[:8]
        try_query = Try.objects.filter(match__in=match_query).order_by('-match__date')

    tries_for_template = []

    for t in try_query:
        tryBlock = templateInfo()
        tryBlock.player_name = t.player.name
        tryBlock.player_pic = t.player.picture
        tryBlock.id = t.id

        tryBlock.player_link = "/player/" + str(t.player.id)
        tryBlock.player_team = t.player.team.team_name
        tryBlock.player_team_link = "/team/" + str(t.player.team.id)
        tryBlock.try_url = t.video_link
        tryBlock.try_match = t.match
        tryBlock.match_link = "/match/" + str(t.match.id)
        tryBlock.video_link = t.video_link
        tryBlock.pic = "https://img.youtube.com/vi/" + str(tryBlock.try_url.split("embed/")[1][:11]) + "/0.jpg"

        if t.match.home_team == t.player.team or t.match.home_team == t.player.internation_team:
            tryBlock.vs = t.match.away_team.team_name
        else:
            tryBlock.vs = t.match.home_team.team_name

        tries_for_template.append(tryBlock)

    return tries_for_template

def prepareMatchData(player_request=None, match_request=None, team_request=None, league_request=None):

    matches = []

    if match_request is not None:
        matches = Match.objects.filter(home_team=match_request.home_team,away_team=match_request.away_team) | Match.objects.filter(home_team=match_request.away_team,away_team=match_request.home_team).order_by('-date')
    elif team_request is not None:
        matches = Match.objects.filter(Q(home_team=team_request) | Q(away_team=team_request)).filter(error=0).order_by('-date')[:8]
    elif league_request is not None:
        matches = Match.objects.filter(league_id=league_request,error=0).order_by('-date')[:8]
    else:
        matches = Match.objects.filter(error=0).order_by('-date')[:8]


    matches_for_template = []

    if len(matches) == 0:
        return matches_for_template

    for m in matches:
        matchBlock = matchInfo()
        matchBlock.video_link = youtube_to_embed(m.video_link)
        matchBlock.match_link = "/match/" + str(m.id)
        matchBlock.home_team = m.home_team.team_name
        matchBlock.away_team = m.away_team.team_name
        matchBlock.id = m.id
        matches_for_template.append(matchBlock)
        matchBlock.pic = "https://img.youtube.com/vi/" + str(matchBlock.video_link.split("embed/")[1][:11]) + "/0.jpg"
        matchBlock.home_link = "/team/" + str(m.home_team.id)
        matchBlock.away_link = "/team/" + str(m.away_team.id)
        matchBlock.date = m.date.date()

    return matches_for_template

def prepareSearchData():

    boxes = []

    for team in Team.objects.all():
        box = searchBox()
        box.name = team.team_name
        box.link = "/team/" + str(team.id)
        boxes.append(box)

    for player in Player.objects.all():
        box = searchBox()
        box.name = player.name
        box.link = "/player/" + str(player.id)
        boxes.append(box)

    return boxes

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
