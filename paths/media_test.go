package paths

import (
	"fmt"
	"io/ioutil"
	"os"
	"path/filepath"
	"testing"
)

const tmpTreeRoot = "testing"

func prepareTestRoot() (string, error) {
	tmp, err := ioutil.TempDir("", tmpTreeRoot)
	if err != nil {
		return "", fmt.Errorf("Could not create temporary dir: %v\n", err)
	}
	return tmp, err
}

func prepareTestTree(tmp, tree string) (string, error) {
	var path = filepath.Join(tmp, tree)
	err := os.MkdirAll(path, 0755)
	if err != nil {
		_ = os.RemoveAll(path)
		return "", err
	}
	empty, err := os.Create(filepath.Join(path, "empty.mkv"))
	if err != nil {
		_ = os.RemoveAll(path)
		return "", err
	}
	_ = empty.Close()
	return path, err
}

func TestWalkRootDirectory(t *testing.T) {
	tmp, err := prepareTestRoot()
	if err != nil {
		t.Error(err)
		return
	}

	tmpA, errA := prepareTestTree(tmp, "TV\\ Series/Oh\\ My\\ Ghost/Season\\ 1")
	tmpB, errB := prepareTestTree(tmp, "Anime/Oh\\ My\\ Goddess/Season\\ 1")
	tmpC, errC := prepareTestTree(tmp, "Movies/Avatar")
	if errA != nil {
		t.Error(errA)
	}
	if errB != nil {
		t.Error(errB)
	}
	if errC != nil {
		t.Error(errC)
	}
	defer os.RemoveAll(tmpA)
	defer os.RemoveAll(tmpB)
	defer os.RemoveAll(tmpC)

	err, paths := WalkRootDirectory(tmp)
	if err != nil {
		t.Error(err)
		return
	}
	if len(paths) != 3 {
		t.Errorf("Root: %s\nDid not find three paths, found %d instead\n%+v",
			os.TempDir(), len(paths), paths)
		return
	}
	if paths[0].Name != "Oh My Goddess" {
		t.Errorf("%s != %s", paths[0].Name, "Oh My Goddess")
	}
	if paths[0].MediaType != MediaTypeAnime {
		t.Errorf("%s %d != Media Type Anime (%d)",
			paths[0].Name, paths[0].MediaType, MediaTypeAnime)
	}
	if paths[1].Name != "Avatar" {
		t.Errorf("%s != %s", paths[1].Name, "Avatar")
	}
	if paths[1].MediaType != MediaTypeMovie {
		t.Errorf("%s %d != Media Type Movie (%d)",
			paths[1].Name, paths[1].MediaType, MediaTypeMovie)
	}
	if paths[2].Name != "Oh My Ghost" {
		t.Errorf("%s != %s", paths[2].Name, "Oh My Ghost")
	}
	if paths[2].MediaType != MediaTypeTV {
		t.Errorf("%s %d != Media Type TV (%d)",
			paths[2].Name, paths[2].MediaType, MediaTypeTV)
	}
}
