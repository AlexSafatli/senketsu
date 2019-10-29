package main

import (
	"./paths"
	"fmt"
	"github.com/fabioberger/airtable-go"
	"os"
)

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

	// Update AirTable
	w, u, d, err := MirrorMediaLocations(split.TV, conf.MediaTables.TV, conn)
	if err != nil {
		panic(err)
	}
	fmt.Printf("Wrote %d records, updated %d records, and deleted %d records -> %s\n",
		w, u, d, conf.MediaTables.TV)
	w, u, d, err = MirrorMediaLocations(split.Movies, conf.MediaTables.Movie, conn)
	if err != nil {
		panic(err)
	}
	fmt.Printf("Wrote %d records, updated %d records, and deleted %d records -> %s\n",
		w, u, d, conf.MediaTables.Movie)
	w, u, d, err = MirrorMediaLocations(split.Anime, conf.MediaTables.Anime, conn)
	if err != nil {
		panic(err)
	}
	fmt.Printf("Wrote %d records, updated %d records, and deleted %d records -> %s\n",
		w, u, d, conf.MediaTables.Anime)
	w, u, d, err = MirrorMediaLocations(split.Dramas, conf.MediaTables.Drama, conn)
	if err != nil {
		panic(err)
	}
	fmt.Printf("Wrote %d records, updated %d records, and deleted %d records -> %s\n",
		w, u, d, conf.MediaTables.Drama)
	w, u, d, err = MirrorMediaLocations(split.Unformatted, conf.MediaTables.Unformatted, conn)
	if err != nil {
		panic(err)
	}
	fmt.Printf("Wrote %d records, updated %d records, and deleted %d records -> %s\n",
		w, u, d, conf.MediaTables.Unformatted)
}

func main() {
	// Check if arg length correct
	if len(os.Args) < 2 || len(os.Args) > 3 {
		fmt.Printf("Usage of %s:\n <root_path> [scan/scrape]\n", os.Args[0])
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
		scan(root, &conf, conn)
	} else if cmd == "scrape" {
		// Do scraping
	}
}
