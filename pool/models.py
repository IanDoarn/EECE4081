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
    name = models.CharField(max_length=64)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return "{}".format(self.name)
    

class Game(models.Model):
    favorite = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='favorite')
    underdog = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='underdog')
    home = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home')
    tv = models.CharField(max_length=12)
    date_time = models.DateTimeField()
    spread = models.FloatField()
    is_game_of_week = models.BooleanField(default=False)
    underdog_score = models.IntegerField(null=True, blank=True)
    favorite_score = models.IntegerField(null=True, blank=True)
    is_tie_breaker = models.BooleanField(default=False)

    class Meta:
        ordering = [
            'date_time'
        ]

    def __str__(self):
        return "{} vs {} on {} at {}".format(
                self.favorite.name,    self.underdog.name,
                self.date_time.date(), self.date_time.time()
            )


class Bet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    is_high_risk = models.BooleanField()
    date_time = models.DateTimeField()
    has_paid_for_season = models.BooleanField(default=False)
    has_paid_for_week = models.BooleanField(default=False)

    class Meta:
        ordering = [
            'date_time',
            'user'
        ]

    def __str__(self):
        return "{}'s bet for {} during \"{}\"".format(
            self.user.username,
            self.team,
            self.game
        )
        

class Season(models.Model):
    name = models.CharField(max_length=128)
    start = models.DateField(default=timezone.now)
    end = models.DateField(default=timezone.now)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    start = models.DateField(default=timezone.now)

    def __str__(self):
        return "{} {}".format(self.user.username, self.start)


class SeasonalSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    season = models.OneToOneField(Season, on_delete=models.CASCADE)

    def __str__(self):
        return "{} {}".format(self.user.username, self.season)


