from django.contrib import admin

# Register your models here.

from .models import Bet, Game, Season, Team, GameUpload, Subscription, SeasonalSubscription

admin.site.register(Bet)
admin.site.register(Game)
admin.site.register(Season)
admin.site.register(Team)
admin.site.register(GameUpload)
admin.site.register(Subscription)
admin.site.register(SeasonalSubscription)
