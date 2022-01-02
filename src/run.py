import logging
from scraping.webpage import WebPage


def main():
    page = WebPage(url="https://en.spitogatos.gr/for_sale-homes/athens-center")


if __name__ == "__main__":
    logging.basicConfig(filename='output.log', level=logging.INFO)
    main()
