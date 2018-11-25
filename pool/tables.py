from django.utils.safestring import mark_safe
from django.utils.html import escape
import django_tables2 as tables


class GameTable(tables.Table):
    id = tables.Column(verbose_name='Place Bet')
    favorite = tables.Column()
    spread = tables.Column()
    underdog = tables.Column()
    date_time = tables.Column(verbose_name='Date / Time')


    def render_id(self, value, record):
        return mark_safe('<button id="button{}" value="game_id_{}" name="game_id_{}" class="btn btn-info">Place Bet</button>'.format(escape(record.id), escape(record.id), escape(record.id)))
