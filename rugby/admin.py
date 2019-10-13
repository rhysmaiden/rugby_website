from django.contrib import admin
from rugby.models import Match
from rugby.models import Player
from rugby.models import Try
from rugby.models import Team
from rugby.models import League

class TryAdmin(admin.ModelAdmin):
  search_fields = ('player__name',)
  ordering = ('-match__date',)

class MatchAdmin(admin.ModelAdmin):
  ordering = ('-date',)  

admin.site.register(Match,MatchAdmin)
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(League)
admin.site.register(Try,TryAdmin)