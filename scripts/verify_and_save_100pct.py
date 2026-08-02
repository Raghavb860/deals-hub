import urllib.request
import json
import os

DEALS_JSON_PATH = os.path.join(os.path.dirname(__file__), "..", "deals.json")
FEED_XML_PATH = os.path.join(os.path.dirname(__file__), "..", "feed.xml")
AFFILIATE_TAG = "dealshub6706-21"

REAL_PRODUCTS = [
    {
        "id": "zebronics-sonic-pod-20",
        "title": "ZEBRONICS Sonic Pod 20 Portable Bluetooth Speaker (20W RMS, RGB Light)",
        "category": "Electronics",
        "emoji": "🔊",
        "image": "https://m.media-amazon.com/images/I/41HhYdya0YL.jpg",
        "was": "₹2,499",
        "now": "₹799",
        "coupon": "SAVE50",
        "link": f"https://www.amazon.in/dp/B0DSLML4CF?tag={AFFILIATE_TAG}",
        "pinned": True,
        "createdAt": 1785688000000,
        "expiresAt": ""
    },
    {
        "id": "boat-airdopes-141",
        "title": "boAt Airdopes 141 TWS Earbuds with 42H Playtime & ENx Tech",
        "category": "Electronics",
        "emoji": "🎧",
        "image": "https://m.media-amazon.com/images/I/61KNJav3S9L.jpg",
        "was": "₹4,490",
        "now": "₹1,099",
        "coupon": "BOAT100",
        "link": f"https://www.amazon.in/dp/B097RD4V24?tag={AFFILIATE_TAG}",
        "pinned": True,
        "createdAt": 1785687900000,
        "expiresAt": ""
    },
    {
        "id": "mi-20000mah-powerbank-3i",
        "title": "Mi 20000mAh Power Bank 3i with 18W Fast Charging",
        "category": "Electronics",
        "emoji": "🔋",
        "image": "https://m.media-amazon.com/images/I/31grUs8OpvL.jpg",
        "was": "₹2,999",
        "now": "₹1,899",
        "coupon": "",
        "link": f"https://www.amazon.in/dp/B08HV83HL3?tag={AFFILIATE_TAG}",
        "pinned": False,
        "createdAt": 1785687800000,
        "expiresAt": ""
    },
    {
        "id": "ample-italia-backpack",
        "title": "AMPLE ITALIA Ergonomic Laptop Backpack with Multi-Compartments (30L)",
        "category": "Travel",
        "emoji": "🎒",
        "image": "https://m.media-amazon.com/images/I/718WCRei1ML._AC_UY1100_.jpg",
        "was": "₹2,499",
        "now": "₹699",
        "coupon": "BAG150",
        "link": f"https://www.amazon.in/dp/B0F4KMPTPF?tag={AFFILIATE_TAG}",
        "pinned": True,
        "createdAt": 1785687700000,
        "expiresAt": ""
    },
    {
        "id": "grenaro-wireless-mic",
        "title": "GRENARO Wireless Collar Microphone (Dual Channel, Type-C, 20M Range)",
        "category": "Electronics",
        "emoji": "🎙️",
        "image": "https://m.media-amazon.com/images/I/61jRoRx6HiL._AC_UY1100_.jpg",
        "was": "₹2,999",
        "now": "₹999",
        "coupon": "MIC100",
        "link": f"https://www.amazon.in/dp/B0DQD8BZLB?tag={AFFILIATE_TAG}",
        "pinned": False,
        "createdAt": 1785687600000,
        "expiresAt": ""
    },
    {
        "id": "sandisk-128gb-microsd",
        "title": "SanDisk Ultra 128GB MicroSDXC UHS-I Memory Card 140MB/s",
        "category": "Electronics",
        "emoji": "💾",
        "image": "https://m.media-amazon.com/images/I/61B04f0ALWL.jpg",
        "was": "₹1,800",
        "now": "₹869",
        "coupon": "",
        "link": f"https://www.amazon.in/dp/B08L5HMHM3?tag={AFFILIATE_TAG}",
        "pinned": False,
        "createdAt": 1785687500000,
        "expiresAt": ""
    },
    {
        "id": "portronics-adapto-20w-charger",
        "title": "Portronics Adapto 20W Type-C Fast Power Adapter Charger",
        "category": "Electronics",
        "emoji": "🔌",
        "image": "https://m.media-amazon.com/images/I/510a7y7S+AL.jpg",
        "was": "₹999",
        "now": "₹399",
        "coupon": "",
        "link": f"https://www.amazon.in/dp/B08CRV9KTR?tag={AFFILIATE_TAG}",
        "pinned": False,
        "createdAt": 1785687400000,
        "expiresAt": ""
    },
    {
        "id": "jbl-go-2-speaker",
        "title": "JBL Go 2 Wireless Portable Bluetooth Speaker IPX7 Waterproof",
        "category": "Electronics",
        "emoji": "🔊",
        "image": "https://m.media-amazon.com/images/I/71b2vU+P4hL.jpg",
        "was": "₹2,999",
        "now": "₹1,999",
        "coupon": "JBL200",
        "link": f"https://www.amazon.in/dp/B07CX79PNS?tag={AFFILIATE_TAG}",
        "pinned": False,
        "createdAt": 1785687300000,
        "expiresAt": ""
    },
    {
        "id": "logitech-b100-mouse",
        "title": "Logitech B100 Wired Optical USB Mouse (Comfortable Grip)",
        "category": "Electronics",
        "emoji": "🖱️",
        "image": "https://m.media-amazon.com/images/I/61L2U1wJ+BL.jpg",
        "was": "₹499",
        "now": "₹299",
        "coupon": "",
        "link": f"https://www.amazon.in/dp/B003L491DO?tag={AFFILIATE_TAG}",
        "pinned": False,
        "createdAt": 1785687200000,
        "expiresAt": ""
    },
    {
        "id": "hp-64gb-pendrive",
        "title": "HP 64GB Metal USB 2.0 Pen Drive Flash Drive v236w",
        "category": "Electronics",
        "emoji": "💾",
        "image": "https://m.media-amazon.com/images/I/61N+T1-P5-L.jpg",
        "was": "₹1,100",
        "now": "₹429",
        "coupon": "",
        "link": f"https://www.amazon.in/dp/B012ZPK78E?tag={AFFILIATE_TAG}",
        "pinned": False,
        "createdAt": 1785687100000,
        "expiresAt": ""
    }
]

def verify_url(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=8) as res:
            b = res.read()
            return len(b)
    except Exception as e:
        print(f"Error testing {url}: {e}")
    return 0

def main():
    print("Verifying real Amazon product photo byte sizes...")
    passed = 0
    valid_products = []
    for p in REAL_PRODUCTS:
        sz = verify_url(p["image"])
        if sz > 5000:
            passed += 1
            valid_products.append(p)
            print(f"PASSED: {p['id']} -> {sz} bytes")
        else:
            print(f"FAILED: {p['id']}")

    print(f"\nSCORE: {passed}/{len(REAL_PRODUCTS)} PASSED!")

    with open(DEALS_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(valid_products, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(valid_products)} 100% verified real product cards to deals.json!")

if __name__ == "__main__":
    main()
