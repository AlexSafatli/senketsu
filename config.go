package senketsu

import "github.com/evalphobia/go-config-loader"

const (
	confType      = "toml"
	basePath      = "config"
	apiKey        = "database.api_key"
	mediaBase     = "media.base_id"
	tvTable       = "media.tv_table_name"
	animeTable    = "media.anime_table_name"
	movieTable    = "media.movie_table_name"
	dramaTable    = "media.drama_table_name"
	watchlistBase = "watchlist.base_id"
)

type configValues struct {
	ApiKey        string
	MediaBase     string
	WatchlistBase string
	MediaTables   struct {
		TV    string
		Anime string
		Movie string
		Drama string
	}
}

func loadConfigs() configValues {
	var conf *config.Config
	conf = config.NewConfig()
	if err := conf.LoadConfigs(basePath, confType); err != nil {
		panic(err)
	}
	return configValues{
		ApiKey:        conf.ValueString(apiKey),
		MediaBase:     conf.ValueString(mediaBase),
		WatchlistBase: conf.ValueString(watchlistBase),
		MediaTables: struct {
			TV    string
			Anime string
			Movie string
			Drama string
		}{
			TV:    conf.ValueString(tvTable),
			Anime: conf.ValueString(animeTable),
			Movie: conf.ValueString(movieTable),
			Drama: conf.ValueString(dramaTable),
		},
	}
}