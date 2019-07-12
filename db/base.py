from path import structure
import scraping.scraper
import tvdb_api


def scrape_media_library_in_db(driver, config):
    updated = []
    for media_type in structure.get_media_library_types():
        table_name = structure.get_media_library_type_label(media_type)
        if table_name is not None:
            conn = driver.new_connection(config, table_name)
            scraper = scraping.scraper.get_scraper_for_media_type(media_type)
            if scraper is not None:
                # Make wrapper interface
                for record in conn.get_all():
                    fields = record['fields']
                    try:
                        s = scraper[fields['Name']]
                        record['fields']['Scrapes To'] = s['seriesname']
                        record['fields']['Rating'] = float(s['siteRating']) if \
                            s['siteRating'] else 0.0
                    except tvdb_api.tvdb_shownotfound:
                        record['fields']['Scrapes To'] = ''
                    updated.append(conn.update(record['id'], record['fields']))
    return len(updated)
