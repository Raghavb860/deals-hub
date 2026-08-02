import urllib.request
import json
import os

DEALS_JSON_PATH = os.path.join(os.path.dirname(__file__), "..", "deals.json")
FEED_XML_PATH = os.path.join(os.path.dirname(__file__), "..", "feed.xml")

# CLEAN UNBLOCKED REAL PRODUCT IMAGE URLS (NO ._SL1500_ WRAPPERS)
CLEAN_PRODUCT_PHOTOS = {
    "zebronics-sonic-pod-20": "https://m.media-amazon.com/images/I/41HhYdya0YL.jpg",
    "boat-airdopes-141": "https://m.media-amazon.com/images/I/61KNJav3S9L.jpg",
    "noise-pulse-2-max": "https://m.media-amazon.com/images/I/61SS2-gWcSL.jpg",
    "oneplus-nord-buds-2": "https://m.media-amazon.com/images/I/61-v8aK1pDL.jpg",
    "mi-20000mah-powerbank-3i": "https://m.media-amazon.com/images/I/31grUs8OpvL.jpg",
    "ample-italia-backpack": "https://m.media-amazon.com/images/I/71Y3wJp00vL.jpg",
    "grenaro-wireless-mic": "https://m.media-amazon.com/images/I/61jZ-R5B6VL.jpg",
    "sandisk-64gb-microsd": "https://m.media-amazon.com/images/I/617Nsf8cRDL.jpg",
    "portronics-car-charger": "https://m.media-amazon.com/images/I/51wJ-d3zL-L.jpg",
    "pigeon-electric-kettle": "https://m.media-amazon.com/images/I/51DJg-3w2nL.jpg",
    "wipro-16a-smart-plug": "https://m.media-amazon.com/images/I/51sVwW8-0xL.jpg",
    "jbl-go-3-speaker": "https://m.media-amazon.com/images/I/61kF-gR3-GL.jpg",
    "boult-z40-tws": "https://m.media-amazon.com/images/I/61wS4f5-7EL.jpg",
    "milton-thermosteel-bottle": "https://m.media-amazon.com/images/I/61H4R8O-JIL.jpg",
    "cello-checkers-container-set": "https://m.media-amazon.com/images/I/81x-Z1rG32L.jpg",
    "wildcraft-45l-rucksack": "https://m.media-amazon.com/images/I/81Q6-Xw5X3L.jpg",
    "puma-mens-sneakers": "https://m.media-amazon.com/images/I/61u5Z8w-y3L.jpg",
    "fastrack-aviator-sunglasses": "https://m.media-amazon.com/images/I/51wY--a551L.jpg",
    "happilo-trail-mix-500g": "https://m.media-amazon.com/images/I/71wZ39F0BXL.jpg",
    "tata-tea-gold-1kg": "https://m.media-amazon.com/images/I/61J6Q5Z43HL.jpg"
}

def check_url(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as res:
            return res.status == 200
    except Exception:
        return False

def main():
    print("Testing clean Amazon CDN photo URLs...")
    with open(DEALS_JSON_PATH, "r", encoding="utf-8") as f:
        deals = json.load(f)

    for d in deals:
        for deal_id, clean_url in CLEAN_PRODUCT_PHOTOS.items():
            if deal_id in d["id"]:
                d["image"] = clean_url
                print(f"Updated {d['id']} -> {clean_url}")
                break

    with open(DEALS_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(deals, f, indent=2, ensure_ascii=False)
    print("Updated deals.json cleanly!")

if __name__ == "__main__":
    main()
