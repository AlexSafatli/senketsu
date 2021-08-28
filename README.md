# senketsu

[Airtable](https://airtable.com)-powered [Plex](https://plex.tv)/[Kodi](https://kodi.tv/)/XBMC Media Library Management and Monitoring using a command line interface (CLI) written in [Go](http://golang.org) and built for simplicity and home server use. Used personally alongside a Plex/Sonarr/Radarr stack. Assumes a partitoning of content in the form of:

- *Dramas* (Asian Dramas including C-Dramas, J-Dramas, K-Dramas)
- *Anime*
- *TV Shows* (anything that is not either of the above two)
- *Movies* (comprising content from any region)

## Current CLI Commands

- `sync`: mirror all Airtable records with media library file metadata

## Planned Features

- (Possible) local storage of findings using [scribble](https://github.com/nanobox-io/golang-scribble)
- Quality recognition
- Sonarr/Radarr integration
- Manage a watch list (akin to [MyAnimeList](http://myanimelist.net)'s) for all of TV Shows, Movies, Asian Dramas, Anime, ....
  - Sync to MyAnimeList for Anime
  - Sync to MyDramaList for Asian Dramas
  - Save to AirTable
  - Save locally

### External APIs

 - TVDB
 - MyAnimeList - [Jikan-go](https://github.com/darenliang/jikan-go)
 - MyDramaList - none - need to scrape HTML or produce own library
