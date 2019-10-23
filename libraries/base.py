import re

import path.helpers
import path.structure
import libraries


__clean_name_regex = r'[^a-zA-Z0-9()\-\' ]'

CLEAN_NAME_REGEX = re.compile(__clean_name_regex)


class MediaLibrary(object):
    def __init__(self, root_path):
        self.root_path = root_path
        self.tv_shows = []
        self.movies = []
        self.anime = []
        self.dramas = []
        self.unformatted = []
        self.__library_paths = path.structure.get_media_library_paths(root_path)
        self.__populate()

    def __len__(self):
        return len(self.tv_shows) + len(self.movies) + len(self.anime) + \
               len(self.dramas)

    def __populate(self):
        for p in self.__library_paths:
            if p.media_type == path.structure.MEDIA_TYPE_TV:
                if p.formatted:
                    self.tv_shows.extend(libraries.tv.get_tv_shows(p))
                else:
                    self.unformatted.extend(libraries.tv.get_tv_shows(p))
            elif p.media_type == path.structure.MEDIA_TYPE_MOVIES:
                if p.formatted:
                    self.movies.extend(libraries.movie.get_movies(p))
                else:
                    self.unformatted.extend(libraries.movie.get_movies(p))
            elif p.media_type == path.structure.MEDIA_TYPE_ANIME:
                if p.formatted:
                    self.anime.extend(libraries.anime.get_anime_shows(p))
                else:
                    self.unformatted.extend(libraries.anime.get_anime_shows(p))
            elif p.media_type == path.structure.MEDIA_TYPE_DRAMA:
                if p.formatted:
                    self.dramas.extend(libraries.dramas.get_dramas(p))
                else:
                    self.unformatted.extend(libraries.dramas.get_dramas(p))

    def get_media_for_media_type(self, media_type):
        if media_type == path.structure.MEDIA_TYPE_TV:
            return self.tv_shows
        elif media_type == path.structure.MEDIA_TYPE_MOVIES:
            return self.movies
        elif media_type == path.structure.MEDIA_TYPE_ANIME:
            return self.anime
        elif media_type == path.structure.MEDIA_TYPE_DRAMA:
            return self.dramas
        return list()


class MediaLocation(path.structure.MediaCenterPath):
    def __init__(self, mpath, mtype):
        super().__init__(mpath, mtype, True)
        self.__size = None
        self.__clean_name = CLEAN_NAME_REGEX.sub('', self.name)
        self.scrape = None

    @property
    def clean_name(self):
        return self.__clean_name

    @property
    def scraped_name(self):
        if self.scrape:
            return self.scrape['seriesname']
        return ''

    @property
    def file_size(self):
        if self.__size is None:
            self.__size = path.helpers.get_folder_size(self.path)
        return self.__size

    def to_dict(self):
        return {
            'Name': self.clean_name,
            'Type': path.structure.get_media_library_type_label(
                self.media_type),
            'Path': self.path,
            'Size': self.file_size * 1.0e-9,
            'Scrapes To': self.scraped_name
        }
