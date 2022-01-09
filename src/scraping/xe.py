import re
import requests
import logging
from pathlib import Path
from typing import Any, Dict, List, Set
from scraping.webpage import WebPage

ROOT_DIR = Path(__file__).parent.parent.parent
IMAGE_DIR = Path(ROOT_DIR, "output", "images")


class Xe_Property(object):
    def __init__(self, cell, get_images: bool = False) -> None:
        self.cell = cell
        self.get_images = get_images
        self.logger = logging.getLogger(f"Property {self.id}")
        self.images: Set[str] = set()
        self.details = self.get_details()

    def __repr__(self) -> str:
        return f"< Property {self.id} >"

    def get_details(self):
        try:
            response = requests.get(self.url)
            result = response.json()["result"]
            if result is None:
                self.logger.warning("unable to get details")
                return None
            self.logger.info(f'Details from "{self.url}" loaded')
            self.download_images(result)
            return self.parse_details(result)
        except requests.exceptions.Timeout as e:
            self.logger.warning(f"Request timeout: {e.response}")
        except requests.exceptions.RequestException as e:
            self.logger.warning(f"Request failed: {e.response}")
        return None

    def parse_details(self, result: Dict[str, Any]):
        return {
            "id": result.get("id", None),
            "bathrooms": result.get("bathrooms", None),
            "bedrooms": result.get("bedrooms", None),
            "condition": result.get("condition", None),
            "furnished": result.get("furnished", None),
            "location_latitude": result.get("geo_lat", None),
            "location_longitude": result.get("geo_lng", None),
            "item_type": result.get("item_type", None),
            "owner_email": result.get("owner_email", None),
            "renovated": result.get("renovated", None),
            "property_type": result.get("type", None),
            "description": result.get("publication_text", None),
            "price_total": self.get_decimal(result, "price"),
            "price_sqm": self.get_decimal(result, "price_per_square_meter"),
            "saves": self.get_decimal(result, "saves"),
            "visits": self.get_decimal(result, "visits"),
            "size_sqm": self.get_decimal(result, "size"),
            "construction_year": self.get_decimal(result, "construction_year"),
        }

    def download_images(self, result: Dict[str, Any]):
        if not self.get_images:
            return
        image_urls: List[str] = result.get("image_gallery", [])
        for url in image_urls:
            try:
                response = requests.get(url)
                filename = url.split("/")[-1]
                self.save_image(response.content, filename)
            except requests.exceptions.Timeout as e:
                self.logger.warning(f"Request timeout: {e.response}")
            except requests.exceptions.RequestException as e:
                self.logger.warning(f"Request failed: {e.response}")

    def save_image(self, image, filename: str):
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
    def get_decimal(result: Dict[str, Any], key: str):
        text = result.get(key, None)
        if text is None:
            return None
        matches = re.findall(r"\d+", text)
        if len(matches) == 0:
            return None
        return int("".join(matches))

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


class Xe(WebPage):
    def __init__(self, url: str) -> None:
        super().__init__(url)
        self.property_dict: Dict[str, Xe_Property] = {}

    def check_for_properties(self, get_images: bool = False):
        cells = self.soup.find_all("div", class_="cell")

        for cell in cells:
            property = Xe_Property(cell, get_images)
            id = property.id
            if id is not None and id not in self.property_dict:
                self.property_dict[id] = property
