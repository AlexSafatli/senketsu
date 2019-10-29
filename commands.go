package main

import (
	"./paths"
	"fmt"
	"github.com/fabioberger/airtable-go"
	"os"
)

func mirror(locs []paths.MediaLocation, table string, conn *airtable.Client) {
	w, u, d, err := MirrorMediaLocations(locs, table, conn)
	if err != nil {
		panic(err)
	}
	fmt.Printf("Wrote %d records, updated %d records, and deleted %d records -> %s\n",
		w, u, d, table)
}

func scan(root string, conf *configValues, conn *airtable.Client) {
	// Do scan
	err, scanned := paths.WalkRootDirectory(root)
	if err != nil {
		panic(err)
	}
	fmt.Printf("Scan complete (%d): ", len(scanned))
	if len(scanned) == 0 {
		fmt.Println("Nothing found. Stopping.")
		os.Exit(0)
	}

	split := paths.SplitIntoMediaTypes(scanned)
	fmt.Printf("%d TV | %d Movies | %d Anime | %d Dramas | %d Unformatted\n",
		len(split.TV), len(split.Movies), len(split.Anime), len(split.Dramas),
		len(split.Unformatted))

	// Update AirTable tables
	mirror(split.TV, conf.MediaTables.TV, conn)
	mirror(split.Movies, conf.MediaTables.Movie, conn)
	mirror(split.Anime, conf.MediaTables.Anime, conn)
	mirror(split.Dramas, conf.MediaTables.Drama, conn)
	mirror(split.Unformatted, conf.MediaTables.Unformatted, conn)
}
