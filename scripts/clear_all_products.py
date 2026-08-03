import json
import os
import xml.etree.ElementTree as ET

DEALS_JSON_PATH = os.path.join(os.path.dirname(__file__), "..", "deals.json")
FEED_XML_PATH = os.path.join(os.path.dirname(__file__), "..", "feed.xml")

def main():
    # 1. Clear deals.json
    with open(DEALS_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump([], f, indent=2)
    print("Cleared deals.json -> []")

    # 2. Clear feed.xml RSS
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = "Deals Hub — Hand-Picked Real Deals & Discounts"
    ET.SubElement(channel, "link").text = "https://raghavb860.github.io/deals-hub/"
    ET.SubElement(channel, "description").text = "Today's best Amazon loot deals & price drops India."

    tree = ET.ElementTree(rss)
    ET.indent(tree, space="  ", level=0)
    tree.write(FEED_XML_PATH, encoding="utf-8", xml_declaration=True)
    print("Cleared feed.xml RSS!")

if __name__ == "__main__":
    main()
