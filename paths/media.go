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
	MediaLabelTV         = "TV Series"
	MediaLabelMovie      = "Movies"
	MediaLabelAnime      = "Anime"
	MediaLabelAsianDrama = "Dramas"
)

type MediaLocation struct {
	MediaType      uint8
	RootPath       string
	Name           string
	Size           uint
	NumberSeasons  uint
	NumberEpisodes uint
	MediaFiles     []string
}

func GetMediaType(path string) uint8 {
	var baseName = filepath.Base(path)
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

func WalkRootDirectory(path string) (err error, paths []MediaLocation) {
	err = filepath.Walk(path, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		} else if info.Name() == path {
			return nil
		}
		var parent = filepath.Dir(info.Name())
		if info.IsDir() && parent != path {
			var loc = MediaLocation{
				RootPath:  info.Name(),
				MediaType: GetMediaType(parent),
				Size:      uint(info.Size()),
			}
			//if err := WalkLocationDirectory(&loc); err != nil {
			//	return nil
			//}
			paths = append(paths, loc)
		} else if parent == path {
			return nil
		}
		return filepath.SkipDir
	})
	return
}

func WalkLocationDirectory(loc *MediaLocation) (err error) {
	err = filepath.Walk(loc.RootPath, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		} else if info.Name() == loc.RootPath {
			return nil
		}
		// TODO do something in the location directory
		return filepath.SkipDir
	})
	return
}
