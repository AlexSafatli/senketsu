import os

import path.structure
from path import helpers
from libraries.base import MediaLocation
import scraping.tv

LABEL_TV_SEASON = 'Season'


class TVShow(MediaLocation):
    def __init__(self, tvpath):
        super().__init__(tvpath, path.structure.MEDIA_TYPE_TV)
        self.seasons = []
        self.other_files = []
        self.__populate()
        self.__scrape()

    def __populate(self):
        for fi in self:
            name = helpers.get_file_name_parts(fi)[0]
            if os.path.isdir(fi) and LABEL_TV_SEASON in name:
                self.seasons.append(TVShowSeason(self, fi))
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


class TVShowSeason(MediaLocation):
    parent = None
    path = ''
    episodes = None

    def __init__(self, parent, spath):
        super().__init__(spath, path.structure.MEDIA_TYPE_CHILD)
        self.parent = parent
        self.episodes = []
        self.__populate()

    def __len__(self):
        return len(self.episodes)

    def __populate(self):
        for fi in self:
            fi_type = helpers.get_file_type(fi)
            if fi_type is not None and 'video' in fi_type.mime:
                self.episodes.append(fi)


def get_tv_shows(tv_path):
    shows = []
    if tv_path.media_type != path.structure.MEDIA_TYPE_TV:
        raise ValueError('No TV shows in non-TV show path')
    for subpath in tv_path:
        shows.append(TVShow(subpath))
    return shows
