package senketsu

import (
	"fmt"
	"os"
)

func main() {
	// Check if arg length correct
	if len(os.Args) < 2 || len(os.Args) > 3 {
		fmt.Printf("Usage of %s:\n <root_path> [sync/scrape]\n", os.Args[0])
		os.Exit(1)
	}

	// Read config file(s)
	conf := loadConfigs()

	// Open AirTable connection to campaign base
	conn, err := OpenConnection(conf.ApiKey, conf.MediaBase)
	if err != nil {
		panic(err)
	}
}
