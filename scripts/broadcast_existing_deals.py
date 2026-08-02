import json
import urllib.request
import time
import os

DEALS_JSON_PATH = os.path.join(os.path.dirname(__file__), "..", "deals.json")
WA_PHONE_NUMBER_ID = "1325947473926027"
WA_ACCESS_TOKEN = "EAAbAYVkv24oBSN7tuqobK3gylBXnEMUnqTZCF0iEYZAz1wUOBElFxO0WqCuv4BhWvBg5l1dGxeysm4aZBitIJ0padH0oNExxBdabcFZB974zPtUD2ZBh4CBczdYogM3OC94e0u7az92l68RZBqx6gn6PhrC1YvC0sSny3ChzBKyZAau1GblIo9zbeh53H4GSgHGdCmMddp6XR943ISOn4cMbVuNbc7NkMHZBJPJDsTZCm1H5iYC9TPv1hAQ8bcrVSxVbf2QazyHYHEw8BI90OaOUs"

def broadcast_deal(d):
    url = f"https://graph.facebook.com/v18.0/{WA_PHONE_NUMBER_ID}/messages"
    msg_body = f"🔥 *AMAZON LOOT DEAL!*\n\n🛍️ *{d['title']}*\n💰 *Price:* {d['now']}"
    if d.get('was'):
        msg_body += f" (Was {d['was']})"
    msg_body += f"\n\n👉 *Grab Deal Here:* {d['link']}\n\n_Shared via Deals Hub_"
    
    headers = {
        "Authorization": f"Bearer {WA_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    # Meta Cloud API message payload
    payload = {
        "messaging_product": "whatsapp",
        "to": "1325947473926027", # Meta test number
        "type": "text",
        "text": { "body": msg_body }
    }

    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers=headers, method='POST')
        with urllib.request.urlopen(req) as res:
            print(f"Sent: {d['title'][:40]}...")
    except Exception as e:
        print(f"Note for '{d['title'][:20]}': {e}")

def main():
    if not os.path.exists(DEALS_JSON_PATH):
        print("deals.json not found.")
        return

    with open(DEALS_JSON_PATH, "r", encoding="utf-8") as f:
        deals = json.load(f)

    print(f"Broadcasting {len(deals)} existing deals to WhatsApp...")
    for d in deals[:10]: # Send top 10 deals
        broadcast_deal(d)
        time.sleep(1) # Rate limit delay

if __name__ == "__main__":
    main()
