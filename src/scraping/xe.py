import re
from typing import Dict
from scraping.webpage import WebPage


class Xe_Property(object):
    def __init__(self, cell) -> None:
        self.cell = cell

    def __repr__(self) -> str:
        return f"< {self.id} | {self.area} | {self.price} | {self.price_per_sqm} >"

    @staticmethod
    def get_decimal(text: str):
        matches = re.findall(r"\d+", text)
        if len(matches) == 0:
            return None
        return int("".join(matches))

    @property
    def area(self):
        span = self.cell.find("span", class_="common-property-ad-address")
        if span is None:
            return None
        return span.text.split("|")[0][15:-1]

    @property
    def price(self):
        span = self.cell.find("span", class_="property-ad-price")
        if span is None:
            return None
        return self.get_decimal(span.text)

    @property
    def price_per_sqm(self):
        span = self.cell.find("span", class_="property-ad-price-per-sqm")
        if span is None:
            return None
        return self.get_decimal(span.text)

    @property
    def id(self):
        a = self.cell.find("a")
        if a is None:
            return None
        match = re.search(r"results/(?P<id>\d+)", a["href"])
        if match is None:
            return None
        return match.group("id")


class Xe(WebPage):
    def __init__(self, url: str) -> None:
        super().__init__(url)
        self.property_dict: Dict[str, Xe_Property] = {}

    def check_for_properties(self):
        cells = self.soup.find_all("div", class_="cell")

        for cell in cells:
            property = Xe_Property(cell)
            id = property.id
            if id is not None and id not in self.property_dict:
                self.property_dict[id] = property
