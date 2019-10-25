package main

import (
	"./paths"
	"fmt"
	"os"
)

func main() {
	// Check if arg length correct
	if len(os.Args) < 2 || len(os.Args) > 3 {
		fmt.Printf("Usage of %s:\n <root_path> [sync/scrape]\n", os.Args[0])
		os.Exit(2)
	}

	// Read config file(s)
	conf := loadConfigs()

	// Open AirTable connection to media base
	conn, err := OpenConnection(conf.ApiKey, conf.MediaBase)
	if err != nil {
		panic(err)
	}

	// Get arguments
	var root = os.Args[1]
	var cmd = os.Args[2]

	// Do scan (scrape currently not implemented)
	if cmd != "scan" && cmd != "scrape" {
		_, _ = fmt.Fprintf(os.Stderr, "Command '%s' not supported", cmd)
		os.Exit(1)
	}
	if cmd == "scan" {
		err, scanned := paths.WalkRootDirectory(root)
		if err != nil {
			panic(err)
		}
		split := paths.SplitIntoMediaTypes(scanned)
		if err = MirrorMediaLocations(split.TV, conf.MediaTables.TV, conn); err != nil {
			panic(err)
		}
		if err = MirrorMediaLocations(split.Movies, conf.MediaTables.Movie, conn); err != nil {
			panic(err)
		}
		if err = MirrorMediaLocations(split.Anime, conf.MediaTables.Anime, conn); err != nil {
			panic(err)
		}
		if err = MirrorMediaLocations(split.Dramas, conf.MediaTables.Drama, conn); err != nil {
			panic(err)
		}
		if err = MirrorMediaLocations(split.Unformatted, conf.MediaTables.Unformatted, conn); err != nil {
			panic(err)
		}
	}
}
