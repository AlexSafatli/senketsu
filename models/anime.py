import os

import path.structure
from path import helpers
from models.base import MediaLocation

LABEL_TV_SEASON = 'Season'


class AnimeShow(MediaLocation):
    seasons = None
    other_files = None

    def __init__(self, tvpath):
        super().__init__(tvpath, path.structure.MEDIA_TYPE_ANIME)
        self.__populate()

    def __populate(self):
        self.seasons = list()
        self.other_files = list()
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
        d['Number of Episodes'] = sum(len(x) for x in self.seasons)
        return d


class AnimeSeason(MediaLocation):
    parent = None
    path = ''
    episodes = None

    def __init__(self, parent, spath):
        super().__init__(spath, path.structure.MEDIA_TYPE_CHILD)
        self.parent = parent
        self.episodes = list()
        self.__populate()

    def __len__(self):
        return len(self.episodes)

    def __populate(self):
        for fi in self:
            name = helpers.get_file_name_parts(fi)[0]
            fi_type = helpers.get_file_type(fi)
            if fi_type is not None and 'video' in fi_type.mime and \
                    'OP' not in name and 'ED' not in name:
                self.episodes.append(fi)


def get_anime_shows(anime_path):
    shows = []
    if anime_path.media_type != path.structure.MEDIA_TYPE_ANIME:
        raise ValueError('No anime in non-anime show path')
    for subpath in anime_path:
        shows.append(AnimeShow(subpath))
    return shows
