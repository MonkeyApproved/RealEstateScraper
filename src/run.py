import logging
from scraping.webpage import WebPage


def main():
    WebPage(url="https://en.spitogatos.gr/for_sale-homes/athens-center", test=123)


if __name__ == "__main__":
    logging.basicConfig(filename="output.log", level=logging.INFO)
    main()
