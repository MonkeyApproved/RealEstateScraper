from scraping.xe import Xe


def test_webpage():
    xe_url = (
        "https://www.xe.gr/property/results?"
        "transaction_name=buy&"
        "item_type=re_residence&"
        "geo_place_id=ChIJ8UNwBh-9oRQR3Y1mdkU1Nic&"
        "maximum_price=150000&"
        "minimum_construction_year=2000&"
        "minimum_level=L1&"
        "minimum_size=70"
    )
    xe = Xe(xe_url)
    xe.check_for_properties(get_images=False)
    assert len(xe.property_dict) > 0
