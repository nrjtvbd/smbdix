import urllib.request
import re
import json

# Configuration
TARGET_IP = "103.165.93.31"
TARGET_PORT = "8095"
BASE_URL = f"http://{TARGET_IP}:{TARGET_PORT}"

def auto_detect_channels_from_server():
    """
    মেইন সার্ভার থেকে সরাসরি চ্যানেল লিস্ট এবং আসল স্লাগ অটো-ক্যাপচার করবে।
    """
    detected_channels = []
    
    # ১. প্রথমে সার্ভারের মূল পেজ বা JSON ফাইল চেক করা
    server_urls_to_try = [
        f"http://{TARGET_IP}/tv_channels.json",
        f"http://{TARGET_IP}/"
    ]
    
    for url in server_urls_to_try:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                content_type = response.headers.get('Content-Type', '')
                data = response.read().decode('utf-8')
                
                # যদি JSON ডাটা পাওয়া যায়
                if 'json' in content_type or url.endswith('.json'):
                    json_data = json.loads(data)
                    channels_list = json_data.get("channels", json_data)
                    for ch in channels_list:
                        name = ch.get("name", "Unknown Channel")
                        category = ch.get("category", "General")
                        
                        # URL বা slug বের করা
                        raw_url = ch.get("url", "")
                        slug_match = re.search(r':8095/([^/]+)', raw_url)
                        slug = slug_match.group(1) if slug_match else name
                        
                        detected_channels.append((name, slug, category))
                    if detected_channels:
                        print(f"✅ JSON থেকে {len(detected_channels)} টি চ্যানেল অটো ক্যাচ করা হয়েছে।")
                        return detected_channels

                # যদি HTML পেজ পাওয়া যায়
                else:
                    # href/src থেকে চ্যানেল স্লাগগুলো এক্সট্রাক্ট করা (যেমন: /sonyAath/index.m3u8)
                    matches = re.findall(r'/([^/]+)/index\.m3u8', data)
                    unique_slugs = list(set(matches))
                    
                    for slug in unique_slugs:
                        # স্লাগ থেকে অটো চ্যানেল নাম তৈরি
                        clean_name = re.sub(r'([a-z])([A-Z])', r'\1 \2', slug) # sonyAath -> sony Aath
                        clean_name = clean_name.replace('_', ' ').replace('-', ' ').title()
                        detected_channels.append((clean_name, slug, "General"))
                        
                    if detected_channels:
                        print(f"✅ HTML স্ক্র্যাপ করে {len(detected_channels)} টি চ্যানেল অটো ক্যাচ করা হয়েছে।")
                        return detected_channels

        except Exception as e:
            continue

    return detected_channels

def generate_m3u():
    # সম্পূর্ণ অটোমেটিক চ্যানেল ফেচিং
    channels = auto_detect_channels_from_server()

    if not channels:
        print("❌ সার্ভার থেকে কোনো চ্যানেল ফেচ করা সম্ভব হয়নি! IP ও Server Status চেক করুন।")
        return

    m3u_content = "#EXTM3U\n"
    print("🚀 Auto-generated playlist তৈরি হচ্ছে...")

    for name, slug, group in channels:
        if ".m3u8" in slug:
            stream_url = f"{BASE_URL}/{slug}"
        else:
            stream_url = f"{BASE_URL}/{slug}/index.m3u8"

        # অটো লোগো ইউআরএল জেনারেট
        logo_slug = slug.split('/')[0].lower()
        logo_url = f"http://{TARGET_IP}/img/channels/{logo_slug}.png"

        m3u_content += f'#EXTINF:-1 tvg-id="{slug}" tvg-name="{name}" tvg-logo="{logo_url}" group-title="{group}", {name}\n'
        m3u_content += f'#EXTVLCOPT:http-referrer=http://{TARGET_IP}/\n'
        m3u_content += f"{stream_url}\n"

    with open("permanent_list.m3u8", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    
    print(f"🎉 সফলভাবে {len(channels)} টি চ্যালের নিখুঁত স্লাগ দিয়ে permanent_list.m3u8 ফাইল তৈরি হয়েছে।")

if __name__ == "__main__":
    generate_m3u()
