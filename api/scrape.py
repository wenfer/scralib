import logging
from urllib.request import Request

from models.models import Scrape


def map_router(app):
    @app.get("/scrape")
    async def hello_world(request: Request):
        scrapes = await Scrape.all()
        logging.info(f"scrapes size is {len(scrapes)}")
        return {"title": "1111111"}
