# Generated by Django 2.1.2 on 2018-10-30 00:52

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('pool', '0007_gameupload'),
    ]

    operations = [
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('end', models.DateTimeField()),
                ('name', models.CharField(max_length=128)),
                ('start', models.DateTimeField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='gameupload',
            options={'ordering': ['upload_date']},
        ),
        migrations.RemoveField(
            model_name='bet',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='gameupload',
            name='game_data',
        ),
        migrations.AddField(
            model_name='game',
            name='favorite_score',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='is_game_of_week',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='game',
            name='is_tie_breaker',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='game',
            name='underdog_score',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='gameupload',
            name='file',
            field=models.FileField(default=None, upload_to='', validators=[django.core.validators.FileExtensionValidator(['xlsx'])]),
        ),
        migrations.AddField(
            model_name='gameupload',
            name='title',
            field=models.CharField(default='Unknown', max_length=128),
        ),
        migrations.AddField(
            model_name='gameupload',
            name='upload_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 30, 0, 52, 0, 899241, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='bet',
            name='game_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pool.Game'),
        ),
        migrations.AlterField(
            model_name='bet',
            name='team_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pool.Team'),
        ),
        migrations.AlterField(
            model_name='bet',
            name='user_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='game',
            name='spread',
            field=models.FloatField(),
        ),
    ]