import requests
import logging
from bs4 import BeautifulSoup


class WebPage(object):

    def __init__(self, url: str, test: int) -> None:
        self.url = url
        self.logger = logging.getLogger(url)
        self.html = self.load_html(url)
        self.soup = self.make_soup(self.html)
        self.test = test

    def load_html(self, url: str):
        try:
            page = requests.get(url)
            self.logger.info(f'URL "{url}" loaded successfully (length {len(page.text)})')
            return page.content
        except requests.exceptions.Timeout as e:
            self.logger.warning(f'Request timeout: {e.response}')
        except requests.exceptions.TooManyRedirects as e:
            self.logger.warning(f'Bad URL: {e.response}')
        except requests.exceptions.RequestException as e:
            self.logger.warning(f'Bad URL: {e.response}')
        
        return ''

    def make_soup(self, html: str):
        return BeautifulSoup(html, "html.parser")
