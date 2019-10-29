# senketsu

[Airtable](https://airtable.com)-powered [Plex](https://plex.tv)/[Kodi](https://kodi.tv/)/XBMC Media Library Management and Monitoring using a command line interface (CLI) written in [Go](http://golang.org) and built for simplicity and home server use.

## Current CLI Commands

- `sync`: mirror all Airtable records with media library file metadata

## Planned Features

- (Possible) local storage of findings using [scribble](https://github.com/nanobox-io/golang-scribble)
- Complex renaming using pattern recognition and empirical rules for anime (look for similar projects; see what is necessary for XBMC vs. Plex)
- Quality recognition
- Manage a watch list (akin to [MyAnimeList](http://myanimelist.net)'s) for all of TV Shows, Movies, Asian Dramas, Anime, ....
  - Sync to MyAnimeList for Anime
  - Sync to MyDramaList for Asian Dramas
  - Save to AirTable
  - Save locally

### External APIs

 - TVDB
 - MyAnimeList - [Jikan-go](https://github.com/darenliang/jikan-go)
 - MyDramaList - none - need to scrape HTML or produce own library
