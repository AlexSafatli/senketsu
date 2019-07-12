import os

import path.structure
from path import helpers
from models.base import MediaLocation
import scraping.tv

LABEL_DRAMAS_SEASON = 'Season'


class DramaShow(MediaLocation):
    seasons = None
    other_files = None

    def __init__(self, tvpath):
        super().__init__(tvpath, path.structure.MEDIA_TYPE_DRAMA)
        self.__populate()
        self.__scrape()

    def __populate(self):
        self.seasons = list()
        self.other_files = list()
        for fi in self:
            name = helpers.get_file_name_parts(fi)[0]
            if os.path.isdir(fi) and LABEL_DRAMAS_SEASON in name:
                self.seasons.append(DramaShowSeason(self, fi))
            else:
                self.other_files.append(fi)

    def __scrape(self):
        self.scrape = scraping.tv.get_tv_show(
            self.clean_name, scraping.tv.get_tvdb_api_connection())

    @property
    def rating(self) -> float:
        if self.scrape:
            return scraping.tv.get_tv_show_rating(self.scrape)
        return 0

    def get_season(self, snum):
        for season in self.seasons:
            if 'Season %d' % snum == season.name:
                return season
        return None

    def to_dict(self):
        d = super().to_dict()
        d['Number of Seasons'] = len(self.seasons)
        d['Number of Episodes'] = sum(len(x) for x in self.seasons)
        d['Rating'] = self.rating
        return d


class DramaShowSeason(MediaLocation):
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
            fi_type = helpers.get_file_type(fi)
            if fi_type is not None and 'video' in fi_type.mime:
                self.episodes.append(fi)


def get_dramas(dramas_path):
    shows = []
    if dramas_path.media_type != path.structure.MEDIA_TYPE_DRAMA:
        raise ValueError('No dramas in non-dramas show path')
    for subpath in dramas_path:
        shows.append(DramaShow(subpath))
    return shows
