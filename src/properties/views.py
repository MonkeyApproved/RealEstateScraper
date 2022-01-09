from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from scraping.xe import Xe


def help(request):
    return render(request, "help.html")


def igmo(request):
    return HttpResponse("Hi this is Igmo")


def scrape_now(request):
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
    properties = xe.check_for_properties(write_to_db=True)
    return HttpResponse(f"Parsed a total of {len(properties)} properties.")
