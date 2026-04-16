import requests
import os

# কনফিগারেশন
TARGET_IP = "198.195.239.50"
TARGET_PORT = "8095"
BASE_URL = f"http://{TARGET_IP}:{TARGET_PORT}"

def get_active_channels():
    # এটি সার্ভারের স্ট্যাটাস বা ডাটাবেজ থেকে তথ্য নেওয়ার চেষ্টা করবে
    # যেহেতু সরাসরি ডাটা নেই, আমরা একটি কমন স্ল্যাগ লিস্ট স্ক্যান করছি
    common_slugs = [
        "StarGold", "StarGold2", "StarSports1", "StarSports2", "TSports",
        "SonyTen1", "SonyTen2", "SonyTen3", "SonySix", "StarJalsha",
        "ZeeBangla", "ColorsBangla", "SonyAath", "ZeeCinema", "StarMovies",
        "Discovery", "AnimalPlanet", "Nick", "Disney", "CartoonNetwork",
        "SomoyTV", "JamunaTV", "IndependentTV", "Channel24"
    ]
    
    active_list = []
    print("🔎 Scanning for active channels on the server...")

    for slug in common_slugs:
        test_url = f"{BASE_URL}/{slug}/index.m3u8"
        try:
            # সার্ভার সচল কি না তা চেক করা
            response = requests.head(test_url, timeout=3)
            if response.status_code == 200:
                print(f"✅ Found: {slug}")
                active_list.append(slug)
        except:
            continue
            
    return active_list

def generate_m3u():
    channels = get_active_channels()
    
    if not channels:
        print("❌ No active channels found on the server.")
        return

    m3u_content = "#EXTM3U\n"
    for slug in channels:
        # নামগুলো সুন্দর করার জন্য ফরম্যাটিং
        display_name = slug.replace("Star", "Star ").replace("Sony", "Sony ").replace("Zee", "Zee ")
        
        stream_url = f"{BASE_URL}/{slug}/index.m3u8"
        m3u_content += f'#EXTINF:-1 tvg-id="{slug}" tvg-name="{display_name}" group-title="Auto Detected", {display_name}\n'
        m3u_content += f'#EXTVLCOPT:http-referrer=http://{TARGET_IP}/\n'
        m3u_content += f"{stream_url}\n"

    with open("permanent_list.m3u8", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    
    print(f"✅ Successfully generated permanent_list.m3u8 with {len(channels)} channels.")

if __name__ == "__main__":
    generate_m3u()
