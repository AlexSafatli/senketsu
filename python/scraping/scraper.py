import path.structure
import scraping.tv


def get_scraper_for_media_type(media_type):
    if media_type == path.structure.MEDIA_TYPE_ANIME or \
            media_type == path.structure.MEDIA_TYPE_DRAMA or \
            media_type == path.structure.MEDIA_TYPE_TV:
        return scraping.tv.get_tvdb_api_connection()
    return None
