import requests
import re
import os

# CONFIGURATION
TARGET_IP = "198.195.239.50"
TARGET_PORT = "8095"
BASE_URL = f"http://{TARGET_IP}:{TARGET_PORT}"

def generate_m3u():
    # smisp.txt file-ti read kora
    try:
        with open("smisp.txt", "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ smisp.txt file-ti pawa jayni!")
        return

    # Regex diye shob channel name ebong slug (slug: StarGold/index.m3u8) ber kora
    # smisp.txt er pattern: { name: "Channel Name", slug: "Channel-Slug" }
    pattern = r'name:\s*"(.*?)",\s*slug:\s*"(.*?)"'
    channels = re.findall(pattern, content)

    if not channels:
        print("❌ Kono channel khuje pawa jayni! Pattern check korun.")
        return

    m3u_content = "#EXTM3U\n"
    print(f"🚀 Found {len(channels)} channels. Generating Playlist...")

    for name, slug in channels:
        # Stream URL toiri (index.m3u8 format-e)
        stream_url = f"{BASE_URL}/{slug}/index.m3u8"
        
        m3u_content += f'#EXTINF:-1 tvg-name="{name}" group-title="BDIX", {name}\n'
        # Player-er jonno proyojoniyo headers
        m3u_content += f'#EXTVLCOPT:http-referrer=http://{TARGET_IP}/\n'
        m3u_content += f'#EXTVLCOPT:http-user-agent=Mozilla/5.0\n'
        m3u_content += f"{stream_url}\n"

    # Playlist file save kora
    with open("permanent_list.m3u8", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    
    print(f"✅ Successfully generated permanent_list.m3u8 with {len(channels)} channels!")

if __name__ == "__main__":
    generate_m3u()
