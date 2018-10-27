from django.contrib import admin

# Register your models here.

from .models import Bet, Game, Team, GameUpload

admin.site.register(Bet)
admin.site.register(Game)
admin.site.register(Team)
admin.site.register(GameUpload)