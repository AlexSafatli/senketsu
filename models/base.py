import path.structure
import models


class MediaLibrary(object):
    _library_paths = []
    root_path = ''
    tv_shows = []
    movies = []
    anime = []

    def __init__(self, root_path):
        self.root_path = root_path
        self._library_paths = path.structure.get_media_library_paths(root_path)
        self._get_tv_shows()
        self._get_movies()
        self._get_anime()

    def __len__(self):
        return len(self.tv_shows) + len(self.movies) + len(self.anime)

    def _get_tv_shows(self):
        for p in self._library_paths:
            if p.formatted is True and \
                    p.media_type == path.structure.MEDIA_TYPE_TV:
                self.tv_shows.extend(models.tv.get_tv_shows(p))

    def _get_movies(self):
        for p in self._library_paths:
            if p.formatted is True and \
                    p.media_type == path.structure.MEDIA_TYPE_MOVIES:
                self.movies.extend(models.movie.get_movies(p))

    def _get_anime(self):
        for p in self._library_paths:
            if p.formatted is True and \
                    p.media_type == path.structure.MEDIA_TYPE_ANIME:
                self.anime.extend(models.anime.get_anime_shows(p))

    def get_media_for_media_type(self, media_type):
        if media_type == path.structure.MEDIA_TYPE_TV:
            return self.tv_shows
        elif media_type == path.structure.MEDIA_TYPE_MOVIES:
            return self.movies
        elif media_type == path.structure.MEDIA_TYPE_ANIME:
            return self.anime
        return []


class MediaCenterRecord(path.structure.MediaCenterPath):
    def __init__(self, mpath, mtype):
        super().__init__(mpath, mtype, True)

    def to_dict(self):
        return {
            'Name': self.name,
            'Type': path.structure.get_media_library_type_label(self.media_type)
        }
