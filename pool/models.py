from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class BettingRoster(models.Model):
    id = models.IntegerField(primary_key=True)
    team_name = models.CharField(max_length=128)
    rival_name = models.CharField(max_length=128)
    is_favorite = models.BooleanField()
    is_underdog = models.BooleanField()
    is_home_team = models.BooleanField()
    tv_station = models.CharField(max_length=10)
    game_date = models.DateTimeField()
    is_game_of_the_week = models.BooleanField(default=False)


class BettingLine(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    line_date = models.DateTimeField(default=timezone.now)


class BettingBet(models.Model):
    id = models.IntegerField(primary_key=True)
    betting_line_id = models.OneToOneField(BettingLine, on_delete=models.CASCADE)
    roster_id = models.OneToOneField(BettingRoster, on_delete=models.CASCADE)
    bet_amount = models.IntegerField()


class BettingPlayer(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    betting_line_id = models.OneToOneField(BettingLine, on_delete=models.CASCADE)