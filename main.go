package main

import (
	"fmt"
	"os"
)

func main() {
	// Check if arg length correct
	if len(os.Args) < 2 || len(os.Args) > 3 {
		fmt.Printf("Usage of %s:\n <root_path> [scan/scrape]\n",
			os.Args[0])
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

	// Perform whatever command was requested
	switch cmd {
	case "scan":
		scan(root, &conf, conn)
		break
	case "scrape":
		break // not implemented yet
	default:
		_, _ = fmt.Fprintf(os.Stderr, "Command '%s' not supported", cmd)
		os.Exit(1)
	}
}
