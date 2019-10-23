# senketsu

[Airtable](https://airtable.com)-powered [Plex](https://plex.tv)/[Kodi](https://kodi.tv/)/XBMC Media Library Management and Monitoring using a command line interface (CLI) written in [Go](http://golang.org) and built for simplicity and home server use.

## Current CLI Commands

- Airtable `database`
  - `sync`: mirror all Airtable records with media library file metadata
  - `scrape`: attaches metadata from database websites to the Airtable records

## Planned Optimizations

- Speed up sync operation (very slow now; constrained by internal scraping)
  - Parallel scraping operations using a worker pool?
  - Profile operation to get more details
- Consider rewrite in another language (project still immature)

## Planned Features

- Local storage of findings
- Complex renaming
- Quality recognition
- Manage a watch list (akin to [MyAnimeList](http://myanimelist.net)'s) for all of TV Shows, Movies, Asian Dramas, Anime, ....
  - Sync to MyAnimeList for Anime
  - Sync to MyDramaList for Asian Dramas
  - Save to AirTable
  - Save locally

### External APIs

 - TVDB
 - MyAnimeList - [JikanPy](https://github.com/AWConant/jikanpy), [Jikan-go](https://github.com/darenliang/jikan-go)
 - MyDramaList - none - need to scrape HTML or produce own library
