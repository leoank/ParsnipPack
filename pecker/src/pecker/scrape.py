"""
Scraping module.

Provide a wrapper for the googlemaps api to scrape palces API
Also, provides a function to create location boundaries for the US
"""

from pprint import pprint

from googlemaps import Client, places, exceptions as gex
from pydantic import Field
from pydantic_settings import BaseSettings

import pandas as pd
import time
from pathlib import Path


class ScraperConfig(BaseSettings):
    google_api_key: str = Field(default="")
    jobs: int = Field(default=20)


def get_times(reviews_df: pd.DataFrame):
    reviews = reviews_df["reviews"]

    oldest_times = []
    for i in range(len(reviews)):
        r_df = pd.DataFrame(reviews.values[i])
        oldest = r_df["time"].min()
        oldest_times.append(oldest)

    return oldest_times


def parse(hits_df: pd.DataFrame, reviews_df: pd.DataFrame):
    oldest_times = get_times(reviews_df)
    locs = [d["location"] for d in list(hits_df["geometry"]) if "location" in d]
    # descs = [d["overview"] for d in list(reviews_df["editorial_summary"]) if "overview" in d]

    full = pd.DataFrame(
        data={
            "name": hits_df["name"],
            "location": locs,
            "rating": hits_df["rating"],
            "serves_veg": reviews_df["serves_vegetarian_food"],
            "time": oldest_times,
        }
    )

    return full


def scrape():
    sconfig = ScraperConfig()
    gmaps = Client(sconfig.google_api_key)

    hits = places.places(
        gmaps,
        query="restaurants",
        location={"lat": 4.231880e01, "lng": -7.108520e01},
        radius=10,
    )
    hits_df = pd.DataFrame.from_dict(hits["results"])
    if "next_page_token" in hits.keys():
        next_token = hits["next_page_token"]

    while True:
        try:
            hits = places.places(
                gmaps,
                query="restaurants",
                location={"lat": 4.231880e01, "lng": -7.108520e01},
                radius=10,
                page_token=next_token,
            )
            hits_df = pd.concat(
                (hits_df, pd.DataFrame(hits["results"])), ignore_index=True, copy=False
            )
            if "next_page_token" in hits.keys():
                next_token = hits["next_page_token"]
            else:
                break

        except gex.ApiError as e:
            time.sleep(1)

    reviews = []
    for i in range(len(hits_df)):
        reviews.append(places.place(gmaps, hits_df.loc[i, "place_id"])["result"])

    reviews_df = pd.DataFrame.from_dict(reviews)

    summary = parse(hits_df, reviews_df)
    summary.to_parquet(Path(__file__).parents[2].joinpath("data/bos_initial.parquet"))

