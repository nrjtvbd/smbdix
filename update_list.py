import os
import re
import json

# Configuration
TARGET_IP = "103.165.93.31"
TARGET_PORT = "8095"
BASE_URL = f"http://{TARGET_IP}:{TARGET_PORT}"

def extract_channels_from_smbdix_txt():
    """
    smbdix.txt (HTML/JS code) theke auto channel name, slug & category Extract korbe.
    """
    channels = []
    file_path = "smbdix.txt"
    
    if not os.path.exists(file_path):
        print("⚠️ smbdix.txt file not found!")
        return channels

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # HTML/JS er bhetor thaka channels array ba JSON pattern catch kora
        # Regex to capture JS object entries if available
        raw_matches = re.findall(r'\{\s*["\']?name["\']?\s*:\s*["\']([^"\']+)["\']\s*,\s*["\']?url["\']?\s*:\s*["\']([^"\']+)["\']\s*,\s*["\']?category["\']?\s*:\s*["\']([^"\']+)["\']', content)
        
        if raw_matches:
            for name, url, cat in raw_matches:
                slug_match = re.search(r'8095/([^/]+)', url)
                slug = slug_match.group(1) if slug_match else name
                channels.append((name, slug, cat))
            return channels

        # Fallback: HTML anchor / option / dataset parse
        slugs = re.findall(r'8095/([^/]+)/index\.m3u8', content)
        unique_slugs = list(dict.fromkeys(slugs)) # Preserve order & remove dupes

        for slug in unique_slugs:
            # Auto format channel name from slug (e.g., sonyAath -> Sony Aath)
            clean_name = re.sub(r'([a-z])([A-Z])', r'\1 \2', slug)
            clean_name = re.sub(r'([a-zA-Z]+)(\d+)', r'\1 \2', clean_name)
            clean_name = clean_name.replace('_', ' ').replace('-', ' ').title()
            channels.append((clean_name, slug, "General"))

    except Exception as e:
        print(f"❌ Error parsing smbdix.txt: {e}")

    return channels

def generate_m3u():
    channels = extract_channels_from_smbdix_txt()

    if not channels:
        print("❌ No channels could be parsed dynamically!")
        return

    m3u_content = "#EXTM3U\n"
    print(f"🚀 Processing {len(channels)} channels dynamically...")

    for name, slug, group in channels:
        if ".m3u8" in slug:
            stream_url = f"{BASE_URL}/{slug}"
        else:
            stream_url = f"{BASE_URL}/{slug}/index.m3u8"

        logo_slug = slug.split('/')[0].lower()
        logo_url = f"http://{TARGET_IP}/img/channels/{logo_slug}.png"

        m3u_content += f'#EXTINF:-1 tvg-id="{slug}" tvg-name="{name}" tvg-logo="{logo_url}" group-title="{group}", {name}\n'
        m3u_content += f'#EXTVLCOPT:http-referrer=http://{TARGET_IP}/\n'
        m3u_content += f"{stream_url}\n"

    # Save to file
    with open("permanent_list.m3u8", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    
    print(f"✅ Success! Updated permanent_list.m3u8 with {len(channels)} channels.")

if __name__ == "__main__":
    generate_m3u()
