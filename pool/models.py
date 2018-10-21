from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Team(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64)


class Game(models.Model):
    id = models.IntegerField(primary_key=True)
    favorite_id = models.IntegerField()
    underdog_id = models.IntegerField()
    home_id = models.IntegerField()
    tv = models.CharField(max_length=12)
    date_time = models.DateTimeField()
    spread = models.IntegerField()


class Bet(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    game_id = models.OneToOneField(Game, on_delete=models.CASCADE)
    team_id = models.OneToOneField(Team, on_delete=models.CASCADE)
    amount = models.FloatField()
    is_high_risk = models.BooleanField()
    date_time = models.DateTimeField()
