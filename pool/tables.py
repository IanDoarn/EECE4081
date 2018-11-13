from django.utils.safestring import mark_safe
from django.utils.html import escape
import django_tables2 as tables


class ButtonColumn(tables.Column):
    empty_values = list()


class GameTable(tables.Table):
    id = tables.Column()
    favorite = tables.Column()
    spread = tables.Column()
    underdog = tables.Column()


    def render_id(self, value, record):
        # _id = "{}_vs_{}".format(escape(record.favorite), escape(record.underdog))
        return mark_safe('<button id="button{}" value="game_id_{}" name="game_id_{}" class="btn btn-info">Submit</button>'.format(escape(record.id), escape(record.id), escape(record.id)))
