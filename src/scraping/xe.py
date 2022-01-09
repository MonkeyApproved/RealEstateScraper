import re
import requests
import logging
from functools import cached_property
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List
from scraping.webpage import WebPage
from properties import models

ROOT_DIR = Path(__file__).parent.parent.parent
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

    def write_to_database(self):
        if self.details is None:
            return

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


class Xe(WebPage):
    def __init__(self, url: str) -> None:
        super().__init__(url)

    def check_for_properties(self, get_images: bool = False, write_to_db: bool = False):
        cells = self.soup.find_all("div", class_="cell")
        properties: Dict[str, XeProperty] = {}

        for cell in cells:
            property = XeProperty(cell)
            id = property.id
            if id is None:
                continue
            properties[id] = property.details
            if get_images:
                property.save_images()
            if write_to_db:
                property.write_to_database()
        return properties
