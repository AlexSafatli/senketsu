package paths

import (
	"os"
	"path/filepath"
	"strings"
)

func WalkRootDirectory(root string) (err error, paths []MediaLocation) {
	var cleanRoot = filepath.Clean(root)
	err = filepath.Walk(cleanRoot, func(path string, info os.FileInfo, err error) error {
		if err != nil || path == cleanRoot || strings.HasPrefix(info.Name(), ".") {
			return nil // ignore hidden files, etc.
		}
		if info.IsDir() && cleanRoot != filepath.Dir(path) {
			var loc = MediaLocation{
				Name:      strings.ReplaceAll(info.Name(), "\\ ", " "),
				RootPath:  path,
				MediaType: GetMediaType(filepath.Dir(path)),
			}
			if err := WalkLocationDirectory(&loc); err != nil {
				return nil
			}
			paths = append(paths, loc)
		} else if cleanRoot == filepath.Dir(path) {
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
		if err != nil || path == loc.RootPath || strings.HasPrefix(info.Name(), ".") {
			return nil // ignore hidden files, etc.
		}
		if loc.MediaType == MediaTypeTV || loc.MediaType == MediaTypeAnime || loc.MediaType == MediaTypeAsianDrama {
			if info.IsDir() && strings.Contains(info.Name(), "Season") {
				seasonCount++
			} else if !info.IsDir() && IsVideoFile(info.Name()) {
				episodeCount++
			}
		}
		loc.Size += float64(info.Size()) / 1e9
		return nil
	})
	loc.NumberEpisodes = episodeCount
	loc.NumberSeasons = seasonCount
	return
}
