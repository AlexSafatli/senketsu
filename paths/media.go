package paths

import (
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
	MediaUnformattedMarker = "Not Formatted"
)

type MediaLocation struct {
	MediaType      uint8   `json:"-"`
	RootPath       string  `json:"Path"`
	Name           string  `json:"Name"`
	Size           float64 `json:"Size"`
	ScrapeName     string  `json:"Scrapes To,omitempty"`
	NumberSeasons  uint    `json:"Number of Seasons,omitempty"`
	NumberEpisodes uint    `json:"Number of Episodes,omitempty"`
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
	if len(ext) > 0 {
		ext = ext[1:] // trim the dot
	}
	return ext == "mkv" || ext == "webm" || ext == "flv" || ext == "vob" ||
		ext == "ogv" || ext == "avi" || ext == "mts" || ext == "m2ts" ||
		ext == "ts" || ext == "mov" || ext == "qt" || ext == "wmv" ||
		ext == "amv" || ext == "mp4" || ext == "m4v" || ext == "mpg" ||
		ext == "mpeg"
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
