import pytest
from scraping.webpage import WebPage


@pytest.mark.parametrize("test_input,expected", [
    (123, 123),
    (22, 22),
    (5, 5),
])
def test_webpage(test_input, expected):
    assert WebPage(url="https://en.spitogatos.gr/for_sale-homes/athens-center", test=test_input).test is expected
