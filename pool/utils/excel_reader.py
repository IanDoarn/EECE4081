"""
This file is designed to scrape the created template for games of the week.

Excel Files have to two sheets, Games and Scores:
    Games sheet lists what games will be played for the specified week
    Scores lists the scored of aforementioned games

Teams with bold face font are the home team

Dates on the sheet are formatted specifically to allow for parsing
"""
import xlrd
from datetime import datetime


class ExcelParser:

    HEADER_BOUNDS = {'row': 3, 'range': 6}
    TABLE_BOUNDS = {'row_start': 4, 'row_end': 18}

    def __init__(self, file, team_data, game_data):
        self.file = file
        self._team_data = team_data
        self._game_data = game_data

    def _get_team(self, name):
        return self._team_data.get(name=name)

    def parse(self):
        book = xlrd.open_workbook(self.file)
        sheet = book.sheet_by_name('Games')

        table = {'games': [], 'game_of_the_week': sheet.cell_value(19, 2)}

        for row in range(self.TABLE_BOUNDS['row_start'], self.TABLE_BOUNDS['row_end']):
            favorite = self._get_team(sheet.cell(row, 1).value)
            line = sheet.cell(row, 2).value
            underdog = self._get_team(sheet.cell(row, 3).value)
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
