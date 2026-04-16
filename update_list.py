import requests
import os

# কনফিগারেশন
TARGET_IP = "198.195.239.50"
TARGET_PORT = "8095"
BASE_URL = f"http://{TARGET_IP}:{TARGET_PORT}"

# smisp.txt থেকে পাওয়া গুরুত্বপূর্ণ চ্যানেলের লিস্ট (আপনি চাইলে আরও বাড়াতে পারেন)
channels = [
    {"name": "STAR GOLD", "slug": "StarGold"},
    {"name": "STAR SPORTS 1", "slug": "StarSports1"},
    {"name": "SONY TEN 1", "slug": "SonyTen1"},
    {"name": "TSPORTS", "slug": "TSports"},
    {"name": "STAR JALSHA", "slug": "StarJalsha"},
    {"name": "ZEE BANGLA", "slug": "ZeeBangla"}
]

def generate_m3u():
    m3u_content = "#EXTM3U\n"
    print("🚀 Generating Permanent Playlist...")

    for ch in channels:
        # সরাসরি লিঙ্ক তৈরি (যেহেতু এখন টোকেন নেই, কিন্তু ভবিষ্যতে থাকলে এখানে জেনারেট করা যাবে)
        stream_url = f"{BASE_URL}/{ch['slug']}/index.m3u8"
        
        m3u_content += f'#EXTINF:-1 tvg-name="{ch["name"]}", {ch["name"]}\n'
        # হেডার যোগ করা যাতে প্লেয়ারে চলতে সুবিধা হয়
        m3u_content += f'#EXTVLCOPT:http-referrer=http://{TARGET_IP}/\n'
        m3u_content += f"{stream_url}\n"

    with open("permanent_list.m3u8", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print("✅ Playlist generated successfully!")

if __name__ == "__main__":
    generate_m3u()
