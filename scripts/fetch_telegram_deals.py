import urllib.request
import re
import json
import html
import time
import os
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

TELEGRAM_CHANNELS = ["EOnDeals", "TIBGDeals"]
AFFILIATE_TAG = "dealshub6706-21"
DEALS_JSON_PATH = os.path.join(os.path.dirname(__file__), "..", "deals.json")
FEED_XML_PATH = os.path.join(os.path.dirname(__file__), "..", "feed.xml")

WA_PHONE_NUMBER_ID = os.getenv("WA_PHONE_NUMBER_ID", "1325947473926027")
WA_ACCESS_TOKEN = os.getenv("WA_ACCESS_TOKEN", "EAAbAYVkv24oBSDSS4r1ZBvhlSBQ2GgkB4A28CwyYrz64cDCd3QzEnzwrZC61miZB5ZA3NdleRhMUBhOEGhsoh72dkgyCyQJZCJoeZCEZCyfhDcr5jJ1zDXs274kTFLiZB8UZACNf74m1cMpP9pDh5XysadkpngZBnIoZAU8VzKIvqE2a6aZBcAUrqW3qGto7KJGuIIKOz9BUEbIEzbDa3Ewl5nIZCLZCgQOB7WpMfUTxMpNjamBigY5Xz9Nh4t35Aej0OtzA0FgCEDAypfIThC1e4ikkrGpAZDZD")
WA_RECIPIENT = os.getenv("WA_RECIPIENT", "918894860316")

def categorize(title):
    t = title.lower()
    if any(k in t for k in ["phone", "laptop", "speaker", "earphone", "headphone", "buds", "smartwatch", "watch", "mic", "power bank", "charger", "cable", "sd card"]):
        return "Electronics", "⚡"
    if any(k in t for k in ["cleaner", "mop", "shelf", "brush", "wiper", "garbage", "mattress", "stand", "fan", "kitchen", "cooker", "chopper", "mixer"]):
        return "Home & Kitchen", "🏠"
    if any(k in t for k in ["shirt", "t-shirt", "pant", "jeans", "shoes", "socks", "kurta", "saree", "dress", "sunglasses", "umbrella"]):
        return "Fashion", "👗"
    if any(k in t for k in ["backpack", "bag", "suitcase", "trolley", "pillow", "luggage"]):
        return "Travel", "🧳"
    if any(k in t for k in ["oil", "salt", "soap", "detergent", "handwash", "shampoo", "food", "tea", "coffee"]):
        return "Grocery & Essentials", "🧴"
    return "Other", "🏷️"

def extract_asin(url):
    m = re.search(r'/(?:dp|gp/product)/([A-Z0-9]{10})', url)
    if m:
        return m.group(1)
    m = re.search(r'asin=([A-Z0-9]{10})', url, re.IGNORECASE)
    if m:
        return m.group(1)
    return None

def resolve_url(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=8) as res:
            return res.geturl()
    except Exception:
        return url

def fetch_real_amazon_photo(asin):
    url = f"https://www.amazon.in/dp/{asin}"
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=6) as res:
            html_text = res.read().decode('utf-8', errors='ignore')
            
            # Extract real photo URL from Amazon landing page
            m = re.search(r'"landingImageUrl":"([^"]+)"', html_text)
            if m:
                return m.group(1).replace("\\/", "/")
                
            m = re.search(r'data-a-dynamic-image="{&quot;(https://m\.media-amazon\.com/images/I/[^&"]+)', html_text)
            if m:
                return m.group(1).replace("\\/", "/")

            m = re.search(r'"large":"(https://m\.media-amazon\.com/images/I/[^"]+)"', html_text)
            if m:
                return m.group(1).replace("\\/", "/")
    except Exception:
        pass
    return f"https://ws-in.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN={asin}&Format=_SL500_&ID=AsinImage&MarketPlace=IN"

def generate_rss(deals):
    try:
        rss = ET.Element("rss", version="2.0")
        channel = ET.SubElement(rss, "channel")
        
        ET.SubElement(channel, "title").text = "Deals Hub — Hand-Picked Real Deals & Discounts"
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
        print("Updated feed.xml RSS successfully!")
    except Exception as e:
        print(f"Error generating RSS: {e}")

def post_deal_to_whatsapp(deal):
    if not WA_ACCESS_TOKEN or not WA_PHONE_NUMBER_ID or not WA_RECIPIENT:
        return

    url = f"https://graph.facebook.com/v18.0/{WA_PHONE_NUMBER_ID}/messages"
    coupon_str = f"\n🎟️ *Coupon Code:* {deal['coupon']}" if deal.get("coupon") else ""
    msg_body = f"🔥 *AMAZON HIGH-DISCOUNT LOOT DEAL!*\n\n🛍️ *{deal['title']}*\n💰 *Price:* {deal['now']} (Was {deal['was']}){coupon_str}\n\n👉 *Grab Deal Here:* {deal['link']}\n\n_Shared via Deals Hub_"
    
    headers = {
        "Authorization": f"Bearer {WA_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": WA_RECIPIENT,
        "type": "text",
        "text": { "body": msg_body }
    }

    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers=headers, method='POST')
        with urllib.request.urlopen(req) as res:
            print(f"Posted to WhatsApp: {deal['title'][:30]}")
    except Exception as e:
        print(f"WhatsApp posting error: {e}")

def fetch_channel_deals(channel):
    url = f"https://t.me/s/{channel}"
    deals = []
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=10) as res:
            content = res.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Error fetching channel {channel}: {e}")
        return []

    posts = content.split('<div class="tgme_widget_message_wrap')
    for post in posts[1:]:
        links = re.findall(r'href="(https?://(?:www\.)?(?:amazon\.in|amzn\.to|amzn\.in)[^"]+)"', post)
        if not links:
            continue
        
        text_match = re.search(r'<div class="tgme_widget_message_text[^"]*">(.*?)</div>', post, re.DOTALL)
        if not text_match:
            continue
        
        clean_text = re.sub(r'<[^>]+>', ' ', text_match.group(1))
        clean_text = html.unescape(clean_text).strip()
        lines = [line.strip() for line in clean_text.split('\n') if line.strip()]
        if not lines:
            continue
        
        title = lines[0][:100]
        prices = re.findall(r'₹\s*([0-9,]+)', clean_text)
        now_price = f"₹{prices[0]}" if len(prices) >= 1 else "Grab Deal"
        was_price = f"₹{prices[1]}" if len(prices) >= 2 else ""

        coupon_match = re.search(r'(?:code|coupon|use)\s*:\s*([A-Z0-9_-]{4,15})', clean_text, re.IGNORECASE)
        coupon_code = coupon_match.group(1).upper() if coupon_match else ""

        for link in links:
            resolved = resolve_url(link) if ('amzn.to' in link or 'amzn.in' in link) else link
            asin = extract_asin(resolved)
            if asin:
                cat, emoji = categorize(title)
                aff_link = f"https://www.amazon.in/dp/{asin}?tag={AFFILIATE_TAG}"
                
                # Fetch REAL photo directly from Amazon
                real_img = fetch_real_amazon_photo(asin)
                
                deals.append({
                    "id": f"tg-{channel.lower()}-{asin}",
                    "title": title,
                    "category": cat,
                    "emoji": emoji,
                    "image": real_img,
                    "was": was_price,
                    "now": now_price,
                    "coupon": coupon_code,
                    "link": aff_link,
                    "pinned": False,
                    "createdAt": int(time.time() * 1000),
                    "expiresAt": ""
                })
                break
    return deals

def main():
    print("Fetching deals from Telegram & Amazon with REAL product photos...")
    existing = []
    if os.path.exists(DEALS_JSON_PATH):
        try:
            with open(DEALS_JSON_PATH, "r", encoding="utf-8") as f:
                existing = json.load(f)
        except Exception:
            existing = []

    existing_ids = {d["id"] for d in existing}
    new_deals = []

    for ch in TELEGRAM_CHANNELS:
        ch_deals = fetch_channel_deals(ch)
        for d in ch_deals:
            if d["id"] not in existing_ids:
                new_deals.append(d)
                existing_ids.add(d["id"])
                post_deal_to_whatsapp(d)

    combined = new_deals + existing
    # Keep up to 40 items
    combined = combined[:40]

    with open(DEALS_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)
    
    generate_rss(combined)
    print(f"Catalog updated! Currently showing {len(combined)} deals with real photos and affiliate links.")

if __name__ == "__main__":
    main()
