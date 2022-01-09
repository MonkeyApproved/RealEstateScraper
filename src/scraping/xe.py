import re
import json
import requests
import logging
from enum import Enum
from functools import cached_property
from pathlib import Path
from typing import Any, Dict, List
from scraping.webpage import WebPage
from properties import models

ROOT_DIR = Path(__file__).parent.parent.parent
DETAILS_DIR = Path(ROOT_DIR, "output", "details")
IMAGE_DIR = Path(ROOT_DIR, "output", "images")


class XeProperty(object):
    def __init__(self, cell) -> None:
        self.cell = cell
        self.logger = logging.getLogger(f"Property {self.id}")

    def __repr__(self) -> str:
        return f"< Property {self.id} >"

    @property
    def id(self):
        a = self.cell.find("a")
        if a is None:
            return None
        match = re.search(r"results/(?P<id>\d+)", a["href"])
        if match is None:
            return None
        return match.group("id")

    @property
    def url(self):
        return f"https://www.xe.gr/property/results/single_result?id={self.id}"

    @cached_property
    def details(self):
        try:
            response = requests.get(self.url)
            result: Dict[str, Any] = response.json()["result"]
            return result
        except requests.exceptions.Timeout as e:
            self.logger.warning(f"Request timeout: {e.response}")
        except requests.exceptions.RequestException as e:
            self.logger.warning(f"Request failed: {e.response}")
        return None

    def save_to_database(self):
        if self.details is None:
            return
        self.logger.info("Saving details to database")

        owner = models.Owner(owner_email=self.details.get("owner_email", None))
        owner.save()

        page_metrics = models.PageMetrics(
            saves=self.get_integer(self.details, "saves"),
            visits=self.get_integer(self.details, "visits"),
        )
        page_metrics.save()

        geo = models.GeoLocation(
            latitude=self.details.get("geo_lat", ""),
            longitude=self.details.get("geo_lng", ""),
        )
        geo.save()

        property = models.XeProperty(
            id=self.details.get("id", None),
            price_total=self.get_integer(self.details, "price"),
            price_sqm=self.get_integer(self.details, "price_per_square_meter"),
            size_sqm=self.get_integer(self.details, "size"),
            construction_year=self.get_integer(self.details, "construction_year"),
            description=self.details.get("publication_text", None),
            bathrooms=self.details.get("bathrooms", None),
            bedrooms=self.details.get("bedrooms", None),
            condition=self.details.get("condition", None),
            furnished=self.get_bool(self.details, "furnished"),
            renovated=self.get_bool(self.details, "renovated"),
            item_type=self.details.get("item_type", None),
            property_type=self.details.get("type", None),
            owner=owner,
            location=geo,
            metrics=page_metrics,
        )
        property.save()

    def save_details_to_disk(self):
        path = Path(DETAILS_DIR, f"{self.id}.json")
        if path.exists():
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w") as file:
            json.dump(self.details, file, indent=4, sort_keys=True)

    @property
    def image_urls(self):
        urls: List[str] = self.details.get("image_gallery", [])
        return urls

    def save_images(self):
        for url in self.image_urls:
            try:
                response = requests.get(url)
                filename = url.split("/")[-1]
                self.save_image_to_disc(response.content, filename)
            except requests.exceptions.Timeout as e:
                self.logger.warning(f"Request timeout: {e.response}")
            except requests.exceptions.RequestException as e:
                self.logger.warning(f"Request failed: {e.response}")

    def save_image_to_disc(self, image, filename: str):
        path = Path(IMAGE_DIR, self.id, filename)
        if path.exists():
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        print(str(path))
        with path.open("wb") as file:
            file.write(image)
        self.logger.info(f'saved image "{filename}"')
        self.images.add(f"{self.id}/{filename}")
        return path

    @staticmethod
    def get_integer(result: Dict[str, Any], key: str):
        text = result.get(key, None)
        if text is None:
            return None
        matches = re.findall(r"\d+", text)
        if len(matches) == 0:
            return None
        return int("".join(matches))

    @staticmethod
    def get_bool(result: Dict[str, Any], key: str):
        value = result.get(key, None)
        if value is None:
            return False
        return bool(value)


class PropertyType(Enum):
    RESIDENCE = "re_residence"
    LAND = "re_land"


class Xe(WebPage):
    def __init__(
        self, type: PropertyType, max_price: int, min_size: int, min_year: int
    ) -> None:
        super().__init__()
        self.url = (
            "https://www.xe.gr/property/results?"
            "transaction_name=buy&"
            f"item_type={type.value}&"
            "geo_place_id=ChIJ8UNwBh-9oRQR3Y1mdkU1Nic&"
            f"maximum_price={max_price}&"
            f"minimum_construction_year={min_year}&"
            f"minimum_size={min_size}"
        )

    def check_for_properties(
        self,
        save_images: bool = False,
        save_to_db: bool = False,
        save_details_to_disc: bool = False,
    ):
        count = 0
        page = 1
        while True:
            self.logger.info(f"Parsing properties from page {page}")
            url_with_page = f"{self.url}&page={page}"
            cells = self.get_soup(url_with_page).find_all("div", class_="cell")
            for cell in cells:
                property = XeProperty(cell)
                id = property.id
                if id is None:
                    # cell does not contain property details
                    continue
                if save_images:
                    property.save_images()
                if save_to_db:
                    property.save_to_database()
                if save_details_to_disc:
                    property.save_details_to_disk()
                count += 1
            page += 1
            if len(cells) < 30:
                # this was the last page of the pagination
                break
        return count
