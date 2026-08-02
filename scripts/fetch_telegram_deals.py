import urllib.request
import re
import json
import html
import time
import os

TELEGRAM_CHANNELS = ["EOnDeals", "TIBGDeals"]
AFFILIATE_TAG = "dealshub6706-21"
DEALS_JSON_PATH = os.path.join(os.path.dirname(__file__), "..", "deals.json")

# META WHATSAPP CLOUD API CREDENTIALS
WA_PHONE_NUMBER_ID = os.getenv("WA_PHONE_NUMBER_ID", "1325947473926027")
WA_ACCESS_TOKEN = os.getenv("WA_ACCESS_TOKEN", "EAAbAYVkv24oBSN7tuqobK3gylBXnEMUnqTZCF0iEYZAz1wUOBElFxO0WqCuv4BhWvBg5l1dGxeysm4aZBitIJ0padH0oNExxBdabcFZB974zPtUD2ZBh4CBczdYogM3OC94e0u7az92l68RZBqx6gn6PhrC1YvC0sSny3ChzBKyZAau1GblIo9zbeh53H4GSgHGdCmMddp6XR943ISOn4cMbVuNbc7NkMHZBJPJDsTZCm1H5iYC9TPv1hAQ8bcrVSxVbf2QazyHYHEw8BI90OaOUs")
WA_RECIPIENT = os.getenv("WA_RECIPIENT", "")  # Recipient phone number (with country code e.g. 919876543210)

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

def post_deal_to_whatsapp(deal):
    if not WA_ACCESS_TOKEN or not WA_PHONE_NUMBER_ID or not WA_RECIPIENT:
        print("WhatsApp API note: WA_RECIPIENT recipient number not set yet, skipping WhatsApp dispatch.")
        return

    url = f"https://graph.facebook.com/v18.0/{WA_PHONE_NUMBER_ID}/messages"
    msg_body = f"🔥 *HOT AMAZON PRICE DROP!*\n\n🛍️ *{deal['title']}*\n💰 *Price:* {deal['now']}\n\n👉 *Grab Deal Here:* {deal['link']}\n\n_Shared via Deals Hub_"
    
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
            print(f"Successfully posted deal '{deal['title'][:30]}' to WhatsApp!")
    except Exception as e:
        print(f"WhatsApp posting log: {e}")

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
        now_price = "Grab Deal"
        was_price = ""
        price_match = re.search(r'₹\s*([0-9,]+)', clean_text)
        if price_match:
            now_price = f"₹{price_match.group(1)}"

        for link in links:
            resolved = resolve_url(link) if ('amzn.to' in link or 'amzn.in' in link) else link
            asin = extract_asin(resolved)
            if asin:
                cat, emoji = categorize(title)
                aff_link = f"https://www.amazon.in/dp/{asin}?tag={AFFILIATE_TAG}"
                img_url = f"https://ws-in.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN={asin}&Format=_SL500_&ID=AsinImage&MarketPlace=IN"
                
                deals.append({
                    "id": f"tg-{channel.lower()}-{asin}",
                    "title": title,
                    "category": cat,
                    "emoji": emoji,
                    "image": img_url,
                    "was": was_price,
                    "now": now_price,
                    "link": aff_link,
                    "pinned": False,
                    "createdAt": int(time.time() * 1000),
                    "expiresAt": ""
                })
                break
    return deals

def main():
    print("Fetching deals from Telegram channels...")
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
                # Auto post fresh deal to WhatsApp
                post_deal_to_whatsapp(d)

    if new_deals:
        print(f"Found {len(new_deals)} new Amazon deals!")
        combined = new_deals + existing
        combined = combined[:60]
        with open(DEALS_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(combined, f, indent=2, ensure_ascii=False)
        print("Updated deals.json successfully!")
    else:
        print("No new deals found.")

if __name__ == "__main__":
    main()
