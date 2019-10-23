import os
import re

from path import helpers


NUMBERS_REGEXP = r'[0-9]*'
BRACKETS_REGEXP = r'\[[a-zA-Z0-9]*\]'


def get_series_name_and_season(file):
    path_spl: str = str(os.path.dirname(file).split('/'))
    series_name = path_spl[-2].replace('\\', '')
    season_name = path_spl[-1].replace('\\', '')
    season_digits = re.findall(NUMBERS_REGEXP, season_name)
    return series_name, int(season_digits[0]) if len(season_digits) > 0 else 0


def get_season_folders(path):
    season_folders = []
    for fi in helpers.get_files_in_path(path):
        name = helpers.get_file_name_parts(fi)[0]
        if os.path.isdir(fi) and name.lower() == 'season':
            season_folders.append(fi)
    return season_folders


def try_tv_show_renames(path):
    mapped_renames = {}
    for fi in helpers.get_files_in_path(path):
        series_name, season = get_series_name_and_season(fi)
        if os.path.isfile(fi) and not fi.endswith('~'):
            mapped_renames[fi] = try_tv_show_rename(fi, series_name, season)


def try_tv_show_rename(file, series_name, season):
    name, ext = helpers.get_file_name_parts(file)
    numbers = [r for r in re.findall(NUMBERS_REGEXP, name) if r.isdigit()]
    for number in numbers:
        index = name.find(number)
        if index != -1:
            name = name[:index] + name[index+len(number):]
    for bracket in re.findall(BRACKETS_REGEXP, name):
        name = name.strip(bracket)
    number = [r for r in re.findall(NUMBERS_REGEXP, name) if r.isdigit()]
    if len(number) < 1 or 'special' in name.lower():
        return file
    return '.'.join(series_name.split(' ')) + '.s%.2de%s' % (season, number) + \
           ext
