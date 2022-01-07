import requests
import logging
from bs4 import BeautifulSoup


class WebPage(object):
    def __init__(self, url: str) -> None:
        self.url = url
        self.logger = logging.getLogger("WebPage")

    @property
    def html(self):
        try:
            page = requests.get(self.url)
            self.logger.info(f'"{self.url}" loaded (length {len(page.text)})')
            return page.content
        except requests.exceptions.Timeout as e:
            self.logger.warning(f"Request timeout: {e.response}")
        except requests.exceptions.RequestException as e:
            self.logger.warning(f"Request failed: {e.response}")
        return ""

    @property
    def soup(self):
        return BeautifulSoup(self.html, "html.parser")
