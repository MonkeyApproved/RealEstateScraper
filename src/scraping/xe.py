import re
import json
import requests
import logging
import time
from django.utils import timezone
from enum import Enum
from functools import cached_property
from pathlib import Path
from typing import Any, Dict, List
from scraping.webpage import WebPage
from scraping.dates import parse_greek_date
from properties import models
from data_manager.models import DataLoad, LoadConfiguration

ROOT_DIR = Path(__file__).parent.parent.parent
DETAILS_DIR = Path(ROOT_DIR, "output", "details")
IMAGE_DIR = Path(ROOT_DIR, "output", "images")


class XeProperty(object):
    def __init__(self, xe_id: int) -> None:
        self.id = xe_id
        self.logger = logging.getLogger(f"{self.id}")

    def __repr__(self) -> str:
        return f"< Property {self.id} >"

    @property
    def url(self):
        return f"https://www.xe.gr/property/results/single_result?id={self.id}"

    @cached_property
    def details(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
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

    def save_to_database(self, data_load: DataLoad):
        if self.details is None:
            self.logger.warning(f'No details available for "{self.id}", skipping...')
            return False

        # for every run we save the current page metrics (clicks/saves)
        self.add_page_metrics_to_database()

        # we also check the list of images and add any new ones
        self.add_image_urls_to_database()

        # now we check if we already have an entry with the same property id
        # containing the latest updates (same "modified" date as current details)
        if self.already_in_database():
            return False
        else:
            self.add_result_to_database(data_load=data_load)
            return True

    def already_in_database(self) -> bool:
        entries = models.XeResult.objects.filter(
            xe_id=self.get_integer("id"),
            modified=self.get_date("modification_date"),
        )
        if entries.count() > 0:
            # entry with matching id and modified date already exists
            # update "last_parsed_on" field to now
            entries.update(last_parsed_on=timezone.now())
            self.logger.info(f'Already in database...')
            return True
        # no matching entry found in database
        return False

    def add_result_to_database(self, data_load: DataLoad):
        result = models.XeResult(
            xe_id=self.get_integer("id"),
            created=self.get_date("creation_date"),
            url=self.get_string("url"),
            modified=self.get_date("modification_date"),
            owner=self.add_owner_to_database(),
            location=self.add_geo_location_to_database(),
            details=self.add_residence_to_database(),
            data_load=data_load
        )
        result.save()
        self.logger.info(f'saved {self.id} - {self.get_string("item_type")}')
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

    @property
    def image_urls(self):
        urls: List[Dict[str, Dict[str, str]]] = self.details.get("image_gallery", [])
        return urls

    def add_image_urls_to_database(self):
        image_list = self.image_urls
        for image in image_list:
            # check if image already in db
            images = models.Image.objects.filter(
                xe_id=self.get_integer("id"),
                small=image['small']['jpeg'],
            )
            if images.count() != 0:
                # image is already in database
                continue
            image_object = models.Image(
                xe_id = self.get_integer("id"),
                small = image['small']['jpeg'],
                medium = image['medium']['jpeg'],
                big=image['big']['jpeg'],
            )
            image_object.save()

    def save_details_to_disk(self):
        path = Path(DETAILS_DIR, f"{self.get_integer('id')}.json")
        if path.exists():
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w") as file:
            json.dump(self.details, file, indent=4, sort_keys=True)


class PropertyType(Enum):
    RESIDENCE = "re_residence"
    LAND = "re_land"


class GeoPlaceId(Enum):
    ATHENS = "ChIJ8UNwBh-9oRQR3Y1mdkU1Nic"


class Xe(WebPage):
    def __init__(
            self,
            type: str,
            geo_place_id: str,
            max_price: int,
            min_year: int = None,
            min_size: int = None,
            min_level: int = None,
    ) -> None:
        super().__init__()
        self.url = (
            "https://www.xe.gr/property/results?"
            f"transaction_name=buy&"
            f"item_type={type}&"
            f"geo_place_id={geo_place_id}&"
            f"maximum_price={max_price}"
        )
        if type == PropertyType.LAND.value:
            self.url += '&building_type_options%5B%5D=plot'
            self.url += '&city_plan_options%5B%5D=included'
        if min_year is not None and type == PropertyType.RESIDENCE.value:
            self.url += f"&minimum_construction_year={min_year}"
        if min_size is not None and type == PropertyType.RESIDENCE.value:
            self.url += f"&minimum_size={min_size}"
        if min_level is not None and type == PropertyType.RESIDENCE.value:
            self.url += f"&minimum_level=L{min_level}"

    @staticmethod
    def get_id_from_cell(cell: str):
        # the property id can be parsed from the link to the result page inside cell
        a = cell.find("a")
        if a is None:
            return None
        match = re.search(r"(poliseis-katoikion|poliseis-gis-oikopedon)/(?P<id>\d+)/", a["href"])
        if match is None:
            return None
        return int(match.group("id"))

    def check_for_properties(
        self,
        load_config: LoadConfiguration,
        only_parse_new: bool = True,
    ):
        data_load = DataLoad(
            url=self.url,
            count_total=0,
            count_new=0,
            completed=False,
            load_config=load_config
        )
        data_load.save()
        page = 0
        while True:
            page += 1
            self.logger.info(f"Parsing properties from page {page}")
            url_with_page = f"{self.url}&page={page}"
            cells = self.get_soup(url_with_page).find_all(
                "div", class_="property-ad-image-container"
            )
            for cell in cells:
                xe_id = self.get_id_from_cell(cell)
                if xe_id is None:
                    continue
                existing_entries = models.XeResult.objects.filter(xe_id=xe_id)
                if existing_entries.count() > 0 and only_parse_new:
                    # only parse new entries for now -> too many requests get blocked
                    existing_entries.update(last_parsed_on=timezone.now())
                    self.logger.info(f'Skipping "{xe_id}" - {existing_entries.count()} matches found in db')
                    continue
                xe_property = XeProperty(xe_id=xe_id)
                is_new = xe_property.save_to_database(data_load=data_load)
                data_load.count_total += 1
                if is_new:
                    data_load.count_new += 1
                time.sleep(10)
            data_load.save()
            self.logger.info(f"On page {page}, {len(cells)} cell elements found.")
            if len(cells) < 30:
                self.logger.info("All done!")
                # this was the last page of the pagination
                break
        data_load.completed = True
        data_load.save()
        return data_load
