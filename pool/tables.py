import django_tables2 as tables
from .models import Game


class GameTable(tables.Table):
    favorite = tables.Column()
    spread = tables.Column()
    underdog = tables.Column()

    # class Meta:
    #     model = Game
    #     attrs = {'class': 'table table-striped'}