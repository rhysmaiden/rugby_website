from django.contrib import admin
from rugby.models import Match
from rugby.models import Player
from rugby.models import Try
from rugby.models import Team
from rugby.models import League

class TryAdmin(admin.ModelAdmin):
  search_fields = ('player__name',)


class MatchAdmin(admin.ModelAdmin):
  ordering = ('-date',)
  search_fields = ('home_team__team_name','away_team__team_name')

class PlayerAdmin(admin.ModelAdmin):
  search_fields = ('name',)


admin.site.register(Match,MatchAdmin)
admin.site.register(Team)
admin.site.register(Player,PlayerAdmin)
admin.site.register(League)
admin.site.register(Try,TryAdmin)