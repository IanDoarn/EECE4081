import xlrd
from datetime import datetime

def get_games_from_template(template_file, team_data):

    HEADER_BOUNDS = {'row': 3, 'range': 6}
    TABLE_BOUNDS = {'row_start': 4, 'row_end': 18}

    book = xlrd.open_workbook(template_file)
    sheet = book.sheet_by_name('Games')

    headers = [sheet.cell(HEADER_BOUNDS['row'], i).value for i in range(1, HEADER_BOUNDS['range'])]
    table = {'games': [], 'game_of_the_week': sheet.cell_value(19, 2)}


    for row in range(TABLE_BOUNDS['row_start'], TABLE_BOUNDS['row_end']):
        favorite = _get_team_id(sheet.cell(row, 1).value, team_data)
        line = sheet.cell(row, 2).value
        underdog = _get_team_id(sheet.cell(row, 3).value, team_data)
        tv = sheet.cell(row, 4).value
        date_time = sheet.cell(row, 5).value

        table['games'].append(
            {
                'favorite': favorite,
                'spread': line,
                'underdog': underdog,
                'tv': tv,
                'date_time': datetime.strptime(date_time + ' ' + str(datetime.now().year), '%a %m/%d %I:%M %p %Y')
            }
        )

    return table


def _get_team_id(team_name, team_data):
    for teams in team_data:
        if team_name == teams.name:
            return teams.id