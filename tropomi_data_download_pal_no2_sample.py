from pystac import Collection
from pystac_client import ItemSearch
import requests

dates = ['2019-08','2019-09','2019-10','2019-11']
geofilter = {
    'type': 'Polygon',
    'coordinates': [[[-124.75, 24.5], [-66.76, 24.5], [-66.76, 40], [-124.75, 40], [-124.75, 24.5]]]
}

for date in dates:
    s5p = Collection.from_file("https://data-portal.s5p-pal.com/cat/sentinel-5p/catalog.json")
    endpoint = s5p.get_single_link("search").target
    items = ItemSearch(endpoint, datetime=date, intersects=geofilter).get_items()

    for index, item in enumerate(items, 1):
        download_url = item.assets["download"].href
        product_filename = item.properties["physical_name"]

        print(f"Downloading {product_filename}...")
        r = requests.get(download_url)
        with open(f"V2/{product_filename}", "wb") as product_file:
            product_file.write(r.content)
        print("Product was downloaded correctly")
        



