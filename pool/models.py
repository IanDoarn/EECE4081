from django.db import models
from django.contrib.auth.models import User


class GameUpload(models.Model):
    title = models.CharField(max_length=128)
    upload_date = models.DateTimeField()
    file = models.FileField()

    class Meta:
        ordering = ["upload_date"]

    def save(self, *args, **kwargs):
        if self.file:
            pass

            # TODO: Add functionality here to read CSV file
            # TODO: and add models to games table
            # print(self.file.name)
            # t = Team(id=2000, name=self.file.name)
            # t.save()

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


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_team = models.OneToOneField(Team, on_delete=models.CASCADE)
    city = models.CharField(max_length=128)

    def __str__(self):
        return "{} ({} {})".format(self.user.username, self.user.first_name, self.user.last_name)
