from django.contrib import admin

# Register your models here.

from .models import Bet, Game, Team

admin.site.register(Bet)
admin.site.register(Game)
admin.site.register(Team)
