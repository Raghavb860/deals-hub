import urllib.request
import json
import os
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

DEALS_JSON_PATH = os.path.join(os.path.dirname(__file__), "..", "deals.json")
FEED_XML_PATH = os.path.join(os.path.dirname(__file__), "..", "feed.xml")
AFFILIATE_TAG = "dealshub6706-21"

NEW_CATEGORIES_CATALOG = [
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
        "createdAt": int(time.time() * 1000),
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
        "createdAt": int(time.time() * 1000) - 1000,
        "expiresAt": ""
    },
    {
        "id": "razer-deathadder-gaming-mouse",
        "title": "Razer DeathAdder Essential Gaming Mouse (6400 DPI Optical Sensor)",
        "category": "Gaming & Accessories",
        "emoji": "🎮",
        "image": "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=600&auto=format&fit=crop&q=80",
        "was": "₹4,499",
        "now": "₹1,299",
        "coupon": "RAZER200",
        "link": f"https://www.amazon.in/s?k=Razer+DeathAdder+Essential+Gaming+Mouse&tag={AFFILIATE_TAG}",
        "pinned": False,
        "createdAt": int(time.time() * 1000) - 1500,
        "expiresAt": ""
    },
    {
        "id": "cosmic-byte-gaming-headset",
        "title": "Cosmic Byte GS430 Gaming Headset with Microphone (RGB LED)",
        "category": "Gaming & Accessories",
        "emoji": "🎧",
        "image": "https://images.unsplash.com/photo-1545454675-3531b543be5d?w=600&auto=format&fit=crop&q=80",
        "was": "₹1,499",
        "now": "₹799",
        "coupon": "GAME100",
        "link": f"https://www.amazon.in/s?k=Cosmic+Byte+GS430+Gaming+Headset&tag={AFFILIATE_TAG}",
        "pinned": False,
        "createdAt": int(time.time() * 1000) - 1800,
        "expiresAt": ""
    },
    {
        "id": "philips-hair-straightener",
        "title": "Philips Selfie Hair Straightener HP8302/00 (SilkPro Care Tech)",
        "category": "Beauty & Personal Care",
        "emoji": "💇‍♀️",
        "image": "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=600&auto=format&fit=crop&q=80",
        "was": "₹1,445",
        "now": "₹999",
        "coupon": "BEAUTY100",
        "link": f"https://www.amazon.in/s?k=Philips+Selfie+Hair+Straightener+HP8302&tag={AFFILIATE_TAG}",
        "pinned": False,
        "createdAt": int(time.time() * 1000) - 1900,
        "expiresAt": ""
    },
    {
        "id": "bombay-shaving-facial-kit",
        "title": "Bombay Shaving Company Charcoal Facial Grooming Kit",
        "category": "Beauty & Personal Care",
        "emoji": "🧔",
        "image": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=600&auto=format&fit=crop&q=80",
        "was": "₹895",
        "now": "₹499",
        "coupon": "SHAVE50",
        "link": f"https://www.amazon.in/s?k=Bombay+Shaving+Company+Charcoal+Facial+Kit&tag={AFFILIATE_TAG}",
        "pinned": False,
        "createdAt": int(time.time() * 1000) - 2000,
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
        "createdAt": int(time.time() * 1000) - 3000,
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
        "link": f"https://www.amazon.in/s?k=SanDisk+Ultra+128GB+MicroSDXC&tag={AFFILIATE_TAG}",
        "pinned": False,
        "createdAt": int(time.time() * 1000) - 4000,
        "expiresAt": ""
    },
    {
        "id": "cadbury-silk-chocolate-pack",
        "title": "Cadbury Dairy Milk Silk Chocolate Gift Pack (350g)",
        "category": "Grocery & Essentials",
        "emoji": "🍫",
        "image": "https://images.unsplash.com/photo-1549007994-cb92caebd54b?w=600&auto=format&fit=crop&q=80",
        "was": "₹500",
        "now": "₹349",
        "coupon": "SILK50",
        "link": f"https://www.amazon.in/s?k=Cadbury+Dairy+Milk+Silk+Chocolate+Gift+Pack&tag={AFFILIATE_TAG}",
        "pinned": False,
        "createdAt": int(time.time() * 1000) - 5000,
        "expiresAt": ""
    },
    {
        "id": "nivea-men-shower-gel-pack",
        "title": "Nivea Men Active Clean Shower Gel 250ml Body Wash",
        "category": "Grocery & Essentials",
        "emoji": "🧴",
        "image": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=600&auto=format&fit=crop&q=80",
        "was": "₹500",
        "now": "₹299",
        "coupon": "NIVEA50",
        "link": f"https://www.amazon.in/s?k=Nivea+Men+Active+Clean+Shower+Gel&tag={AFFILIATE_TAG}",
        "pinned": False,
        "createdAt": int(time.time() * 1000) - 6000,
        "expiresAt": ""
    },
    {
        "id": "pigeon-electric-kettle",
        "title": "Pigeon by Stovekraft Amaze Plus 1.5 Litre Electric Kettle (1500W)",
        "category": "Home & Kitchen",
        "emoji": "🫖",
        "image": "https://images.unsplash.com/photo-1544816155-12df9643f363?w=600&auto=format&fit=crop&q=80",
        "was": "₹1,295",
        "now": "₹549",
        "coupon": "KETTLE50",
        "link": f"https://www.amazon.in/s?k=Pigeon+by+Stovekraft+Amaze+Plus+Electric+Kettle&tag={AFFILIATE_TAG}",
        "pinned": False,
        "createdAt": int(time.time() * 1000) - 7000,
        "expiresAt": ""
    },
    {
        "id": "solimo-nonstick-cookware-set",
        "title": "Solimo Non-Stick Cookware 3-Piece Set (Fry Pan, Kadhai, Tawa)",
        "category": "Home & Kitchen",
        "emoji": "🍳",
        "image": "https://images.unsplash.com/photo-1584992236310-6edddc08acff?w=600&auto=format&fit=crop&q=80",
        "was": "₹2,500",
        "now": "₹1,149",
        "coupon": "SOLIMO100",
        "link": f"https://www.amazon.in/s?k=Solimo+Non-Stick+Cookware+3-Piece+Set&tag={AFFILIATE_TAG}",
        "pinned": False,
        "createdAt": int(time.time() * 1000) - 8000,
        "expiresAt": ""
    },
    {
        "id": "american-tourister-backpack",
        "title": "American Tourister 32L Casual Laptop Backpack (Water Resistant)",
        "category": "Travel",
        "emoji": "🎒",
        "image": "https://images.unsplash.com/photo-1622560480605-d83c853bc5c3?w=600&auto=format&fit=crop&q=80",
        "was": "₹2,800",
        "now": "₹999",
        "coupon": "AT100",
        "link": f"https://www.amazon.in/s?k=American+Tourister+32L+Casual+Laptop+Backpack&tag={AFFILIATE_TAG}",
        "pinned": False,
        "createdAt": int(time.time() * 1000) - 9000,
        "expiresAt": ""
    },
    {
        "id": "puma-mens-sneakers",
        "title": "Puma Men's Smash v2 Leather Casual Sneakers",
        "category": "Fashion",
        "emoji": "👟",
        "image": "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=600&auto=format&fit=crop&q=80",
        "was": "₹4,999",
        "now": "₹2,199",
        "coupon": "PUMA300",
        "link": f"https://www.amazon.in/s?k=Puma+Men%27s+Smash+v2+Leather+Casual+Sneakers&tag={AFFILIATE_TAG}",
        "pinned": False,
        "createdAt": int(time.time() * 1000) - 10000,
        "expiresAt": ""
    }
]

def verify_url(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=6) as res:
            b = res.read()
            return len(b)
    except Exception as e:
        print(f"Error testing {url}: {e}")
    return 0

def generate_rss(deals):
    try:
        rss = ET.Element("rss", version="2.0")
        channel = ET.SubElement(rss, "channel")
        
        ET.SubElement(channel, "title").text = "Deals Hub — Hand-Picked Real Deals & Discounts"
        ET.SubElement(channel, "link").text = "https://raghavb860.github.io/deals-hub/"
        ET.SubElement(channel, "description").text = "Today's best Amazon loot deals & price drops India."

        for d in deals:
            item = ET.SubElement(channel, "item")
            ET.SubElement(item, "title").text = f"{d['title']} - {d['now']} (Was {d.get('was','')})"
            ET.SubElement(item, "link").text = d["link"]
            ET.SubElement(item, "guid").text = d["id"]
            
            desc = f"🔥 Price Drop: {d['now']}"
            if d.get("was"):
                desc += f" (MRP: {d['was']})"
            if d.get("coupon"):
                desc += f" | 🎟️ Coupon: {d['coupon']}"
            desc += f"\n\nGrab deal: {d['link']}"
            
            ET.SubElement(item, "description").text = desc
            ET.SubElement(item, "pubDate").text = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")

        tree = ET.ElementTree(rss)
        ET.indent(tree, space="  ", level=0)
        tree.write(FEED_XML_PATH, encoding="utf-8", xml_declaration=True)
        print("Updated feed.xml RSS successfully!")
    except Exception as e:
        print(f"Error generating RSS: {e}")

def main():
    print("Verifying 100% byte sizes for all deals including Gaming & Beauty categories...")
    passed = 0
    valid_deals = []

    for p in NEW_CATEGORIES_CATALOG:
        sz = verify_url(p["image"])
        if sz > 5000:
            passed += 1
            valid_deals.append(p)
            print(f"PASSED: {p['id']} -> {sz} bytes")
        else:
            print(f"FAILED: {p['id']}")

    print(f"\nSCORE: {passed}/{len(NEW_CATEGORIES_CATALOG)} PASSED!")

    if passed == len(NEW_CATEGORIES_CATALOG):
        with open(DEALS_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(valid_deals, f, indent=2, ensure_ascii=False)
        generate_rss(valid_deals)
        print(f"PERFECT! Saved {len(valid_deals)} verified products to deals.json!")

if __name__ == "__main__":
    main()
