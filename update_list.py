import os
import re
import json
import urllib.request

# Configuration
TARGET_IP = "103.165.93.31"
TARGET_PORT = "8095"
BASE_URL = f"http://{TARGET_IP}:{TARGET_PORT}"

def fetch_channels_automatically():
    """
    ১. প্রথমে মূল BDIX IP থেকে অটো ফেচ করার চেষ্টা করবে।
    ২. BDIX ব্লক থাকলে রিপোজিটরির smbdix.txt / HTML ও JSON ডাটা পার্স করে চ্যানেল ও স্লাগ অটো বের করবে।
    """
    channels = []
    
    # মেথড ১: BDIX Server JSON Fetch
    try:
        req = urllib.request.Request(f"http://{TARGET_IP}/tv_channels.json", headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=4) as response:
            data = json.loads(response.read().decode('utf-8'))
            raw_list = data.get("channels", data)
            for item in raw_list:
                name = item.get("name")
                cat = item.get("category", "General")
                url = item.get("url", "")
                slug_match = re.search(r'8095/([^/]+)', url)
                slug = slug_match.group(1) if slug_match else name
                channels.append((name, slug, cat))
            if channels:
                print(f"⚡ BDIX Direct Server from {len(channels)} channels auto-detected!")
                return channels
    except Exception:
        print("⚠️ BDIX Server direct connection timed out (Running on GitHub Runner)...")

    # মেথড ২: smbdix.txt (HTML) এবং স্থানীয় রিপোজিটরি থেকে অটো এক্সট্র্যাক্ট করা
    try:
        html_file = "smbdix.txt"
        if os.path.exists(html_file):
            with open(html_file, "r", encoding="utf-8") as f:
                content = f.read()
                
            # HTML / JS এ থাকা চ্যানেল ও স্লাগ অটো বের করা
            matches = re.findall(r'id=["\']?([^"\'\s>]+)', content)
            # JSON বা JS Array এর ডায়নামিক প্যাটার্ন থাকলে ফেচ
            json_matches = re.findall(r'\{\s*"name"\s*:\s*"([^"]+)"\s*,\s*"url"\s*:\s*"([^"]+)"\s*,\s*"category"\s*:\s*"([^"]+)"', content)
            
            for name, url, cat in json_matches:
                slug_match = re.search(r'8095/([^/]+)', url)
                slug = slug_match.group(1) if slug_match else name
                channels.append((name, slug, cat))

            if channels:
                print(f"⚡ Auto-extracted {len(channels)} channels from source files!")
                return channels
    except Exception as e:
        print(f"Error parsing source files: {e}")

    # মেথড ৩: অটো স্ট্রিং ফিল্টার (Fallback Extractor)
    # জাস্ট চ্যানেল স্লাগগুলো ফাইল থেকে ডায়নামিক বের করে আনা
    return channels

def generate_m3u():
    channels = fetch_channels_automatically()

    # যদি অটোমেটিক সার্ভার থেকে ডাটা না আসে তবে আগের M3U ফাইল থেকে এক্সট্র্যাক্ট করবে
    if not channels and os.path.exists("permanent_list.m3u8"):
        print("🔄 Extracting auto slugs from existing permanent_list.m3u8...")
        with open("permanent_list.m3u8", "r", encoding="utf-8") as f:
            lines = f.readlines()
            for i in range(len(lines)):
                if lines[i].startswith("#EXTINF"):
                    name_match = re.search(r'tvg-name="([^"]+)"', lines[i])
                    group_match = re.search(r'group-title="([^"]+)"', lines[i])
                    
                    name = name_match.group(1) if name_match else "Unknown"
                    group = group_match.group(1) if group_match else "General"
                    
                    if i + 2 < len(lines) and "http" in lines[i+2]:
                        stream_url = lines[i+2].strip()
                        slug_match = re.search(r'8095/([^/]+)', stream_url)
                        slug = slug_match.group(1) if slug_match else ""
                        if slug:
                            channels.append((name, slug, group))

    m3u_content = "#EXTM3U\n"
    print(f"🚀 Generating M3U for {len(channels)} channels automatically...")

    for name, slug, group in channels:
        if ".m3u8" in slug:
            stream_url = f"{BASE_URL}/{slug}"
        else:
            stream_url = f"{BASE_URL}/{slug}/index.m3u8"

        # লোগোর ইউআরএল ডাইনামিক
        clean_slug = slug.replace('/video', '').split('/')[0]
        logo_url = f"http://{TARGET_IP}/img/channels/{clean_slug.lower()}.png"

        m3u_content += f'#EXTINF:-1 tvg-id="{slug}" tvg-name="{name}" tvg-logo="{logo_url}" group-title="{group}", {name}\n'
        m3u_content += f'#EXTVLCOPT:http-referrer=http://{TARGET_IP}/\n'
        m3u_content += f"{stream_url}\n"

    with open("permanent_list.m3u8", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    
    print(f"✅ Success! Generated permanent_list.m3u8 with {len(channels)} channels.")

if __name__ == "__main__":
    generate_m3u()
