from django.shortcuts import render
from django.http import HttpResponse
from scraping.xe import PropertyType, Xe


def help(request):
    return render(request, "help.html")


def igmo(request):
    return HttpResponse("Hi this is Igmo")


def scrape_now(request):
    xe = Xe(
        type=PropertyType.RESIDENCE,
        max_price=150000,
        min_size=90,
        min_year=2000,
    )
    count = xe.check_for_properties(
        save_details_to_disc=True, save_images=False, save_to_db=True
    )
    return HttpResponse(f"Parsed a total of {count} properties.")
