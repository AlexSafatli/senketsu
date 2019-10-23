package paths

type MediaDirectory struct {
	MediaType uint8
	RootPath  string
}

type MediaLocation struct {
	MediaDirectory
	Name           string
	Size           uint
	NumberSeasons  uint
	NumberEpisodes uint
	MediaFiles     []string
}
