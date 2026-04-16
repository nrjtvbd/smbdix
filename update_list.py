import os
import re

# CONFIGURATION
TARGET_IP = "198.195.239.50"
TARGET_PORT = "8095"
BASE_URL = f"http://{TARGET_IP}:{TARGET_PORT}"

def generate_m3u():
    file_path = "smisp.txt"
    
    if not os.path.exists(file_path):
        print(f"❌ Error: {file_path} পাওয়া যায়নি!")
        return

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"❌ ফাইল পড়তে সমস্যা হচ্ছে: {e}")
        return

    # আপনার ফাইলের ফরম্যাট: { name: "Star Gold", slug: "StarGold", ... }
    # এখানে কোটেশন মার্ক একক (') বা দ্বৈত (") হতে পারে, তাই দুইটাই হ্যান্ডেল করা হয়েছে।
    pattern = r'name:\s*["\']([^"\']+)["\'],\s*slug:\s*["\']([^"\']+)["\']'
    channels = re.findall(pattern, content)

    if not channels:
        print("⚠️ কোনো চ্যানেল পাওয়া যায়নি। প্যাটার্নটি ম্যানুয়ালি চেক করা হচ্ছে...")
        # বিকল্প প্যাটার্ন যদি স্পেস বা কমা ভিন্ন থাকে
        pattern_alt = r'name\s*:\s*["\'](.*?)["\']\s*,\s*slug\s*:\s*["\'](.*?)["\']'
        channels = re.findall(pattern_alt, content)

    if not channels:
        print("❌ শেষ চেষ্টাতেও কোনো চ্যানেল মেলেনি। smisp.txt ফাইলের ফরম্যাট ঠিক আছে তো?")
        return

    m3u_content = "#EXTM3U\n"
    print(f"🚀 {len(channels)}টি চ্যানেল পাওয়া গেছে। প্লেলিস্ট তৈরি হচ্ছে...")

    for name, slug in channels:
        # স্টার গোল্ড বা এই জাতীয় নাম থেকে এক্সট্রা স্পেস ক্লিন করা
        clean_name = name.strip()
        clean_slug = slug.strip()
        
        stream_url = f"{BASE_URL}/{clean_slug}/index.m3u8"
        
        m3u_content += f'#EXTINF:-1 tvg-id="{clean_slug}" tvg-name="{clean_name}" group-title="BDIX", {clean_name}\n'
        # হেডার হিসেবে রেফারার এবং ইউজার এজেন্ট যোগ করা
        m3u_content += f'#EXTVLCOPT:http-referrer=http://{TARGET_IP}/\n'
        m3u_content += f'#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\n'
        m3u_content += f"{stream_url}\n"

    # প্লেলিস্ট সেভ করা
    output_file = "permanent_list.m3u8"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(m3u_content)
    
    print(f"✅ সফলভাবে {output_file} তৈরি হয়েছে! মোট চ্যানেল: {len(channels)}")

if __name__ == "__main__":
    generate_m3u()
