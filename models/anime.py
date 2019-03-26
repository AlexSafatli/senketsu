import os

import path.structure
from path import helpers
from .base import MediaCenterRecord

LABEL_TV_SEASON = 'Season'


class AnimeShow(MediaCenterRecord):
    seasons = []
    other_files = []

    def __init__(self, tvpath):
        super().__init__(tvpath, path.structure.MEDIA_TYPE_ANIME)
        self._populate()

    def _populate(self):
        for fi in self:
            name = helpers.get_file_name_parts(fi)[0]
            if os.path.isdir(fi) and LABEL_TV_SEASON in name:
                self.seasons.append(AnimeSeason(self, fi))
            else:
                self.other_files.append(fi)
        self.seasons.sort()

    def get_season(self, snum):
        for season in self.seasons:
            if 'Season %d' % snum == season.name:
                return season
        return None

    def to_dict(self):
        d = super().to_dict()
        d['Number of Seasons'] = len(self.seasons)
        return d


class AnimeSeason(MediaCenterRecord):
    parent = None
    path = ''

    def __init__(self, parent, spath):
        super().__init__(spath, path.structure.MEDIA_TYPE_CHILD)
        self.parent = parent


def get_anime_shows(anime_path):
    shows = []
    if anime_path.media_type != path.structure.MEDIA_TYPE_ANIME:
        raise ValueError('No anime in non-anime show path')
    for subpath in anime_path:
        shows.append(AnimeShow(subpath))
    return shows
