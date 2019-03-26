import os

import path.structure
from path import helpers
from models.base import MediaCenterRecord

LABEL_TV_SEASON = 'Season'


class AnimeShow(MediaCenterRecord):
    seasons = None
    other_files = None

    def __init__(self, tvpath):
        super().__init__(tvpath, path.structure.MEDIA_TYPE_ANIME)
        self.seasons = list()
        self.other_files = list()
        self._populate()

    def _populate(self):
        for fi in self:
            name = helpers.get_file_name_parts(fi)[0]
            if os.path.isdir(fi) and LABEL_TV_SEASON in name:
                self.seasons.append(AnimeSeason(self, fi))
            else:
                self.other_files.append(fi)

    def get_season(self, snum):
        for season in self.seasons:
            if 'Season %d' % snum == season.name:
                return season
        return None

    def to_dict(self):
        d = super().to_dict()
        d['Number of Seasons'] = len(self.seasons)
        d['Number of Episodes'] = sum(map(lambda x: len(x), self.seasons))
        return d


class AnimeSeason(MediaCenterRecord):
    parent = None
    path = ''
    episodes = list()

    def __init__(self, parent, spath):
        super().__init__(spath, path.structure.MEDIA_TYPE_CHILD)
        self.parent = parent
        self._populate()

    def __len__(self):
        return len(self.episodes)

    def _populate(self):
        for fi in self:
            name = helpers.get_file_name_parts(fi)[0]
            fi_type = helpers.get_file_type(fi)
            if 'video' in fi_type.mime and \
                    'OP' not in name and 'ED' not in name:
                self.episodes.append(fi)


def get_anime_shows(anime_path):
    shows = []
    if anime_path.media_type != path.structure.MEDIA_TYPE_ANIME:
        raise ValueError('No anime in non-anime show path')
    for subpath in anime_path:
        shows.append(AnimeShow(subpath))
    return shows
