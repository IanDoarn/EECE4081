from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from .utils.excel_reader import ExcelParser

class GameUpload(models.Model):
    title = models.CharField(max_length=128, default="Unknown")
    upload_date = models.DateTimeField()
    file = models.FileField(default=None, validators=[FileExtensionValidator(['xlsx'])])

    class Meta:
        ordering = ["upload_date"]

    def save(self, *args, **kwargs):
        if self.file:
            ep = ExcelParser(self.file.path, Team.objects.all(), Game.objects.all())

            # TODO: find a way to specify which games to update based on if we are
            # TODO: Adding new games to the table or updating old ones with scores

            # NOTE: This only works for uploading new games but DOES NOT CHECK if
            # NOTE: if those games are are already in the table

            games = ep.parse()

            for game in games['games']:
                g = Game(
                    favorite=game['favorite'],
                    underdog=game['underdog'],
                    home=game['underdog'],
                    tv=game['tv'],
                    spread=game['spread'],
                    date_time=game['date_time'],
                    is_game_of_week=False,
                    underdog_score=None,
                    favorite_score=None,
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
    favorite = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='favorite_id')
    underdog = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='underdog_id')
    home = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_id')
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    is_high_risk = models.BooleanField()
    date_time = models.DateTimeField()

    def __str__(self):
        return "{} ({} {})".format(
            self.user.username,
            str(self.game),
            self.game.date_time
        )


class Season(models.Model):
    id = models.IntegerField(primary_key=True)
    end = models.DateTimeField()
    name = models.CharField(max_length=128)
    start = models.DateTimeField()

    def __str__(self):
        return self.name
