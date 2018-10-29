from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from .utils.excel_reader import get_games_from_template

class GameUpload(models.Model):
    title = models.CharField(max_length=128)
    upload_date = models.DateTimeField()
    file = models.FileField(validators=[FileExtensionValidator(['xlsx'])])

    class Meta:
        ordering = ["upload_date"]

    def save(self, *args, **kwargs):
        if self.file:
            games = get_games_from_template(self.file.path, Team.objects.all())

            _id = max([g.id for g in Game.objects.all()])

            for game in games['games']:
                _id += 1
                g = Game(
                    id=_id,
                    favorite_id=Team.objects.get(id=game['favorite']),
                    underdog_id=Team.objects.get(id=game['underdog']),
                    home_id=Team.objects.get(id=game['underdog']),
                    tv=game['tv'],
                    spread=game['spread'],
                    date_time=game['date_time'],
                    is_game_of_week=False,
                    underdog_score=0,
                    favorite_score=0,
                    is_tie_breaker=False
                )
                g.save()

        super(GameUpload, self).save(*args, **kwargs)

    def __str__(self):
        return self.file.name


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
    spread = models.FloatField()
    is_game_of_week = models.BooleanField(default=False)
    underdog_score = models.IntegerField(null=True, blank=True)
    favorite_score = models.IntegerField(null=True, blank=True)
    is_tie_breaker = models.BooleanField(default=False)

    def __str__(self):
        return "{} vs {}".format(self.favorite_id.name, self.underdog_id.name)


class Bet(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE)
    is_high_risk = models.BooleanField()
    date_time = models.DateTimeField()

    def __str__(self):
        return "{} ({} {})".format(
            self.user_id.username,
            str(self.game_id),
            self.game_id.date_time
        )
