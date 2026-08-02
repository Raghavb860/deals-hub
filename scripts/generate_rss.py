import json
import xml.etree.ElementTree as ET
import os
import time
from datetime import datetime, timezone

DEALS_JSON_PATH = os.path.join(os.path.dirname(__file__), "..", "deals.json")
FEED_XML_PATH = os.path.join(os.path.dirname(__file__), "..", "feed.xml")

def generate_rss():
    if not os.path.exists(DEALS_JSON_PATH):
        return

    with open(DEALS_JSON_PATH, "r", encoding="utf-8") as f:
        deals = json.load(f)

    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    
    ET.SubElement(channel, "title").text = "Deals Hub — Hand-Picked Deals & Discounts"
    ET.SubElement(channel, "link").text = "https://raghavb860.github.io/deals-hub/"
    ET.SubElement(channel, "description").text = "Today's best Amazon loot deals & price drops India."

    for d in deals[:30]:
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
    print("RSS Feed feed.xml created successfully!")

if __name__ == "__main__":
    generate_rss()
