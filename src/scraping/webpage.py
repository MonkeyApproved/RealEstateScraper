import requests
import logging
from bs4 import BeautifulSoup


class WebPage(object):
    def __init__(self) -> None:
        self.logger = logging.getLogger("WebPage")

    def get_html(self, url: str):
        try:
            page = requests.get(url)
            self.logger.info(f'"{url}" loaded (length {len(page.text)})')
            return page.content
        except requests.exceptions.Timeout as e:
            self.logger.warning(f"Request timeout: {e.response}")
        except requests.exceptions.RequestException as e:
            self.logger.warning(f"Request failed: {e.response}")
        return ""

    def get_soup(self, url: str):
        return BeautifulSoup(self.get_html(url), "html.parser")
