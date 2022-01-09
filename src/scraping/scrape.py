from bs4 import BeautifulSoup
import requests
import csv

# Get the source code of the website
url = (
    "https://www.xe.gr/property/results?"
    "transaction_name=buy&"
    "item_type=re_residence&"
    "geo_place_id=ChIJ8UNwBh-9oRQR3Y1mdkU1Nic&"
    "maximum_price=150000&"
    "minimum_construction_year=2000&"
    "minimum_level=L1&"
    "minimum_size=70"
)
source = requests.get(url).text
soup = BeautifulSoup(source, "lxml")

area = []
for in_area in soup.find_all("span", class_="common-property-ad-address"):
    area.append(in_area.text.split("|")[0][15:-1])
print(area)

total_price = []
price_per_sqm = []
for price in soup.find_all("div", class_="common-property-ad-price"):
    total = price.find("span", class_="property-ad-price").text[:-1]
    total_price.append(total[:-1])

    p_per_sqm = price.find("span", class_="property-ad-price-per-sqm").text[17:22]
    p_per_sqm = p_per_sqm.replace(".", "")
    price_per_sqm.append(p_per_sqm)
print(total_price)
print(price_per_sqm)

# find the corresponding link
link_to_ad = []
for ad_link in soup.find_all("div", class_="common-property-ad-body"):
    link_to_ad.append(ad_link.find("a")["href"])
print(link_to_ad)

# For now, write the data in a csv file. Later I will make a website host
with open("prices.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(("area", "total_price", "price_per_sqm", "link"))
    writer.writerows(zip(area, total_price, price_per_sqm, link_to_ad))
