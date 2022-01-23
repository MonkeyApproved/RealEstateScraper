import re
import json
import requests
import logging
from django.utils import timezone
from enum import Enum
from functools import cached_property
from pathlib import Path
from typing import Any, Dict, List
from scraping.webpage import WebPage
from scraping.dates import parse_greek_date
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
        # the property id can be parsed from the link to the result page inside cell
        a = self.cell.find("a")
        if a is None:
            return None
        match = re.search(r"poliseis-katoikion/(?P<id>\d+)/", a["href"])
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

    def get_integer(self, key: str):
        text = self.details.get(key, None)
        if text is None:
            return None
        matches = re.findall(r"\d+", text)
        if len(matches) == 0:
            return None
        return int("".join(matches))

    def get_bool(self, key: str):
        value = self.details.get(key, None)
        if value is None:
            return False
        return bool(value)

    def get_string(self, key: str):
        return self.details.get(key, None)

    def get_date(self, key: str):
        date_string = self.details.get(key, None)
        if date_string is None:
            return None
        return parse_greek_date(date_string)

    def save_to_database(self):
        if self.details is None:
            return

        # for every run we save the current page metrics (clicks/saves)
        self.add_page_metrics_to_database()

        # now we check if we already have an entry with the same property id
        # containing the latest updates (same "modified" date as current details)
        if self.already_in_database():
            self.logger.info("Already exists")
        else:
            self.add_result_to_database()
            self.logger.info("Added to database")

    def already_in_database(self) -> bool:
        entries = models.XeResult.objects.filter(
            xe_id=self.get_integer("id"),
            modified=self.get_date("modification_date"),
        )
        count = entries.count()
        if count > 0:
            # entry with matching id and modified date already exists
            # update "last_parsed_on" field to now
            matching_entry = entries.get()
            matching_entry.last_parsed_on = timezone.now()
            matching_entry.save()
            return True
        # no matching entry found in database
        return False

    def add_result_to_database(self):
        result = models.XeResult(
            xe_id=self.get_integer("id"),
            created=self.get_date("creation_date"),
            modified=self.get_date("modification_date"),
            owner=self.add_owner_to_database(),
            location=self.add_geo_location_to_database(),
            details=self.add_residence_to_database(),
        )
        result.save()
        return result

    def add_residence_to_database(self):
        residence = models.XeResidence(
            price_total=self.get_integer("price"),
            price_sqm=self.get_integer("price_per_square_meter"),
            size_sqm=self.get_integer("size_with_square_meter"),
            construction_year=self.get_integer("construction_year"),
            area=self.get_string("address"),
            description=self.get_string("publication_text"),
            bathrooms=self.get_string("bathrooms"),
            bedrooms=self.get_string("bedrooms"),
            commercial=self.get_bool("is_commercial"),
            item_type=self.get_string("item_type"),
            property_type=self.get_string("type"),
        )
        residence.save()
        return residence

    def add_page_metrics_to_database(self):
        page_metrics = models.PageMetrics(
            xe_id=self.get_integer("id"),
            saves=self.get_integer("saves"),
            visits=self.get_integer("visits"),
        )
        page_metrics.save()
        return page_metrics

    def add_owner_to_database(self):
        owner = models.Owner(
            account_id=self.get_integer("account_id"),
            email=self.get_string("owner_email"),
            address=self.get_string("owner_address"),
            ref_id=self.get_string("customer_ref_id"),
            company_title=self.get_string("company_title"),
            active_ads=self.get_integer("active_ads"),
        )
        owner.save()
        return owner

    def add_geo_location_to_database(self):
        geo = models.GeoLocation(
            latitude=self.get_string("geo_lat"),
            longitude=self.get_string("geo_lng"),
        )
        geo.save()
        return geo

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
        page = 0
        while True:
            page += 1
            self.logger.info(f"Parsing properties from page {page}")
            url_with_page = f"{self.url}&page={page}"
            cells = self.get_soup(url_with_page).find_all(
                "div", class_="property-ad-image-container"
            )
            for cell in cells:
                property = XeProperty(cell)
                id = property.id
                if id is None:
                    # self.logger.info(f"no id found for {cell}")
                    # cell does not contain property details
                    continue
                if save_images:
                    property.save_images()
                if save_to_db:
                    property.save_to_database()
                if save_details_to_disc:
                    property.save_details_to_disk()
                count += 1
            cell_count = len(cells)
            self.logger.info(f"On page {page}, {cell_count} cell elements found.")
            self.logger.info(f"A total of {count} properties have been parsed.")
            if len(cells) < 30:
                self.logger.info(f"All done!")
                # this was the last page of the pagination
                break
        return count
