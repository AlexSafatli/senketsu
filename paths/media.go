package paths

import (
	"os"
	"path/filepath"
	"strings"
)

const (
	MediaTypeUnk        uint8 = iota
	MediaTypeTV         uint8 = iota
	MediaTypeMovie      uint8 = iota
	MediaTypeAnime      uint8 = iota
	MediaTypeAsianDrama uint8 = iota
)

const (
	MediaLabelTV           = "TV Series"
	MediaLabelMovie        = "Movies"
	MediaLabelAnime        = "Anime"
	MediaLabelAsianDrama   = "Dramas"
	MediaUnformattedMarker = "Unformatted"
)

type MediaLocation struct {
	MediaType      uint8   `json:"Type"`
	RootPath       string  `json:"Path"`
	Name           string  `json:"Name"`
	Size           float64 `json:"Size"`
	NumberSeasons  uint    `json:"Number of Seasons"`
	NumberEpisodes uint    `json:"Number of Episodes"`
	MediaFiles     []string
}

type MediaLocationsSplit struct {
	TV          []MediaLocation
	Movies      []MediaLocation
	Anime       []MediaLocation
	Dramas      []MediaLocation
	Unformatted []MediaLocation
}

func (l *MediaLocation) ParentDirName() string {
	return filepath.Dir(l.RootPath)
}

func GetMediaType(path string) uint8 {
	var baseName = strings.ReplaceAll(filepath.Base(path), "\\ ", " ")
	if strings.Contains(baseName, MediaLabelTV) {
		return MediaTypeTV
	} else if strings.Contains(baseName, MediaLabelMovie) {
		return MediaTypeMovie
	} else if strings.Contains(baseName, MediaLabelAnime) {
		return MediaTypeAnime
	} else if strings.Contains(baseName, MediaLabelAsianDrama) {
		return MediaTypeAsianDrama
	}
	return MediaTypeUnk
}

func IsVideoFile(basename string) bool {
	var ext = filepath.Ext(basename)
	return ext == "mkv" || ext == "webm" || ext == "flv" || ext == "vob" ||
		ext == "ogv" || ext == "avi" || ext == "mts" || ext == "m2ts" ||
		ext == "ts" || ext == "mov" || ext == "qt" || ext == "wmv" ||
		ext == "amv" || ext == "mp4" || ext == "m4v" || ext == "mpg" ||
		ext == "mpeg"
}

func WalkRootDirectory(root string) (err error, paths []MediaLocation) {
	err = filepath.Walk(root, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		} else if path == root {
			return nil
		}
		var parent = filepath.Dir(path)
		if info.IsDir() && root != parent {
			var loc = MediaLocation{
				Name:      strings.ReplaceAll(info.Name(), "\\ ", " "),
				RootPath:  path,
				MediaType: GetMediaType(parent),
				Size:      float64(info.Size()) / 1e9,
			}
			if err := WalkLocationDirectory(&loc); err != nil {
				return nil
			}
			paths = append(paths, loc)
		} else if root == parent {
			return nil
		}
		return filepath.SkipDir
	})
	return
}

func WalkLocationDirectory(loc *MediaLocation) (err error) {
	var seasonCount uint = 0
	var episodeCount uint = 0
	err = filepath.Walk(loc.RootPath, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		} else if path == loc.RootPath {
			return nil
		}
		if loc.MediaType == MediaTypeTV ||
			loc.MediaType == MediaTypeAnime ||
			loc.MediaType == MediaTypeAsianDrama {
			if info.IsDir() && strings.Contains(info.Name(), "Season") {
				seasonCount++
			} else if !info.IsDir() &&
				strings.Contains(filepath.Dir(path), "Season") &&
				IsVideoFile(info.Name()) {
				episodeCount++
			}
		}
		return filepath.SkipDir
	})
	loc.NumberEpisodes = episodeCount
	loc.NumberSeasons = seasonCount
	return
}

func SplitIntoMediaTypes(locations []MediaLocation) MediaLocationsSplit {
	var tv, movie, anime, drama, unf []MediaLocation
	for i := range locations {
		if strings.Contains(locations[i].ParentDirName(), MediaUnformattedMarker) {
			unf = append(unf, locations[i])
			continue
		}
		switch locations[i].MediaType {
		case MediaTypeTV:
			tv = append(tv, locations[i])
			break
		case MediaTypeMovie:
			movie = append(movie, locations[i])
			break
		case MediaTypeAnime:
			anime = append(anime, locations[i])
			break
		case MediaTypeAsianDrama:
			drama = append(drama, locations[i])
			break
		}
	}
	return MediaLocationsSplit{tv, movie, anime, drama, unf}
}
