from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return "{} ({})".format(self.name, str(self.id))


class Game(models.Model):
    id = models.IntegerField(primary_key=True)
    favorite_id = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='favorite_id')
    underdog_id = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='underdog_id')
    home_id = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_id')
    tv = models.CharField(max_length=12)
    date_time = models.DateTimeField()
    spread = models.IntegerField()

    def __str__(self):
        return "{} vs {}".format(self.favorite_id.name, self.underdog_id.name)


class Bet(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    game_id = models.OneToOneField(Game, on_delete=models.CASCADE)
    team_id = models.OneToOneField(Team, on_delete=models.CASCADE)
    amount = models.FloatField()
    is_high_risk = models.BooleanField()
    date_time = models.DateTimeField()
