import requests
import re
import os

# CONFIGURATION
TARGET_IP = "198.195.239.50"
TARGET_PORT = "8095"
BASE_URL = f"http://{TARGET_IP}:{TARGET_PORT}"

def generate_m3u():
    # ফাইলটি খোলার চেষ্টা করা
    file_path = "smisp.txt"
    
    if not os.path.exists(file_path):
        print(f"❌ Error: {file_path} পাওয়া যায়নি! নিশ্চিত করুন ফাইলটি আপলোড করা হয়েছে।")
        return

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"❌ ফাইল পড়তে সমস্যা হচ্ছে: {e}")
        return

    # আপনার দেওয়া smisp.txt ফাইলের ফরম্যাট অনুযায়ী Regex
    # { name: "Star Gold", slug: "StarGold", category: "movies" } - এই ফরম্যাট থেকে ডাটা নেবে
    pattern = r'name:\s*"([^"]+)",\s*slug:\s*"([^"]+)"'
    channels = re.findall(pattern, content)

    if not channels:
        print("⚠️ কোনো চ্যানেল পাওয়া যায়নি। Regex প্যাটার্ন চেক করুন।")
        return

    m3u_content = "#EXTM3U\n"
    print(f"🚀 {len(channels)}টি চ্যানেল পাওয়া গেছে। প্লেলিস্ট তৈরি হচ্ছে...")

    for name, slug in channels:
        stream_url = f"{BASE_URL}/{slug}/index.m3u8"
        
        m3u_content += f'#EXTINF:-1 tvg-id="{slug}" tvg-name="{name}" group-title="BDIX", {name}\n'
        m3u_content += f'#EXTVLCOPT:http-referrer=http://{TARGET_IP}/\n'
        m3u_content += f'#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)\n'
        m3u_content += f"{stream_url}\n"

    # প্লেলিস্ট সেভ করা
    output_file = "permanent_list.m3u8"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(m3u_content)
    
    print(f"✅ সফলভাবে {output_file} তৈরি হয়েছে!")

if __name__ == "__main__":
    generate_m3u()
