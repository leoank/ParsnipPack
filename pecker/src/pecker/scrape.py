"""
Scraping module.

Provide a wrapper for the googlemaps api to scrape palces API
Also, provides a function to create location boundaries for the US
"""

from pprint import pprint

from googlemaps import Client, places
from pydantic import Field
from pydantic_settings import BaseSettings


class ScraperConfig(BaseSettings):
    google_api_key: str = Field(default="")
    jobs: int = Field(default=20)


def scrape():
    sconfig = ScraperConfig()
    gmaps = Client(sconfig.google_api_key)
    out = places.places(gmaps, query="restaurants")
    out = places.place(gmaps, out["results"][0]["place_id"])
    pprint(out)
