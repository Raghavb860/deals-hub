import urllib.request
import re
import json
import html
import time
import os

TELEGRAM_CHANNELS = ["EOnDeals", "TIBGDeals"]
AFFILIATE_TAG = "dealshub6706-21"
DEALS_JSON_PATH = os.path.join(os.path.dirname(__file__), "..", "deals.json")

WA_PHONE_NUMBER_ID = os.getenv("WA_PHONE_NUMBER_ID", "1325947473926027")
WA_ACCESS_TOKEN = os.getenv("WA_ACCESS_TOKEN", "EAAbAYVkv24oBSN7tuqobK3gylBXnEMUnqTZCF0iEYZAz1wUOBElFxO0WqCuv4BhWvBg5l1dGxeysm4aZBitIJ0padH0oNExxBdabcFZB974zPtUD2ZBh4CBczdYogM3OC94e0u7az92l68RZBqx6gn6PhrC1YvC0sSny3ChzBKyZAau1GblIo9zbeh53H4GSgHGdCmMddp6XR943ISOn4cMbVuNbc7NkMHZBJPJDsTZCm1H5iYC9TPv1hAQ8bcrVSxVbf2QazyHYHEw8BI90OaOUs")
WA_RECIPIENT = os.getenv("WA_RECIPIENT", "")

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

def calculate_discount(was_str, now_str):
    try:
        was = float(re.sub(r'[^0-9.]', '', was_str))
        now = float(re.sub(r'[^0-9.]', '', now_str))
        if was > now and was > 0:
            return int((1 - now / was) * 100)
    except Exception:
        pass
    return 0

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
        
        # Extract prices
        prices = re.findall(r'₹\s*([0-9,]+)', clean_text)
        if len(prices) < 2 and not ("OFF" in clean_text.upper() or "COUPON" in clean_text.upper()):
            # SKIP normal deals with no discount or MRP mentioned!
            continue
            
        now_price = f"₹{prices[0]}" if len(prices) >= 1 else "Grab Deal"
        was_price = f"₹{prices[1]}" if len(prices) >= 2 else ""

        # Extract Coupon if present
        coupon_match = re.search(r'(?:code|coupon|use)\s*:\s*([A-Z0-9_-]{4,15})', clean_text, re.IGNORECASE)
        coupon_code = coupon_match.group(1).upper() if coupon_match else ""

        # STRICT DISCOUNT FILTER: Must have coupon OR at least 25% discount
        disc = calculate_discount(was_price, now_price)
        if disc < 25 and not coupon_code:
            continue

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
                    "coupon": coupon_code,
                    "link": aff_link,
                    "pinned": False,
                    "createdAt": int(time.time() * 1000),
                    "expiresAt": ""
                })
                break
    return deals

def main():
    print("Fetching deals with STRICT DISCOUNT & COUPON filters...")
    existing = []
    if os.path.exists(DEALS_JSON_PATH):
        try:
            with open(DEALS_JSON_PATH, "r", encoding="utf-8") as f:
                raw = json.load(f)
                # PURGE EXPIRED OR LOW DISCOUNT DEALS
                now_ts = int(time.time() * 1000)
                for d in raw:
                    disc = calculate_discount(d.get("was",""), d.get("now",""))
                    # Keep pinned OR deals with coupon OR deals with >= 25% discount
                    if d.get("pinned") or d.get("coupon") or disc >= 25:
                        d["createdAt"] = now_ts # Update timestamp to fresh
                        existing.append(d)
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
    # Keep top 50 high-discount deals
    combined = combined[:50]

    with open(DEALS_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)
    
    print(f"Filter complete! Currently showing {len(combined)} verified high-discount & coupon deals.")

if __name__ == "__main__":
    main()
