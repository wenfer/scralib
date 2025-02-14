from typing import Dict, Optional

from models.movie import Movie


class Scraper:
    pass

    def site_url(self):
        raise NotImplementedError()

    def scrape(self, filename: str) -> Optional[Dict]:
        raise NotImplementedError()
