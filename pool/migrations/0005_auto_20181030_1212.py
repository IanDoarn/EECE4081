# Generated by Django 2.1.1 on 2018-10-30 17:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pool', '0004_auto_20181030_1205'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bet',
            old_name='game_id',
            new_name='game',
        ),
        migrations.RenameField(
            model_name='bet',
            old_name='team_id',
            new_name='team',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='favorite_id',
            new_name='favorite',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='home_id',
            new_name='home',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='underdog_id',
            new_name='underdog',
        ),
    ]