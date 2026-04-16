import os
import re

# কনফিগারেশন
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

    # জাভাস্ক্রিপ্ট অবজেক্টের ভেতর থেকে ডাটা টেনে আনার সবচেয়ে শক্তিশালী Regex
    # এটি name: "...", slug: "..." সব ফরম্যাট ধরবে
    names = re.findall(r'name\s*:\s*["\'](.*?)["\']', content)
    slugs = re.findall(r'slug\s*:\s*["\'](.*?)["\']', content)

    if not names or not slugs:
        print("❌ কোনো ডাটা খুঁজে পাওয়া যায়নি। ফাইলের ফরম্যাটটি সম্ভবত বদলে গেছে।")
        return

    # নাম এবং স্ল্যাগ এর সংখ্যা সমান করার জন্য জিপ করা
    channels = list(zip(names, slugs))

    m3u_content = "#EXTM3U\n"
    print(f"🚀 {len(channels)}টি চ্যানেল পাওয়া গেছে। প্লেলিস্ট তৈরি হচ্ছে...")

    for name, slug in channels:
        # অপ্রয়োজনীয় ক্যারেক্টার ক্লিন করা
        clean_name = name.strip()
        clean_slug = slug.strip()
        
        stream_url = f"{BASE_URL}/{clean_slug}/index.m3u8"
        
        m3u_content += f'#EXTINF:-1 tvg-id="{clean_slug}" tvg-name="{clean_name}" group-title="SM BDIX", {clean_name}\n'
        # প্লেয়ারের জন্য হেডার
        m3u_content += f'#EXTVLCOPT:http-referrer=http://{TARGET_IP}/\n'
        m3u_content += f"{stream_url}\n"

    # আউটপুট ফাইল সেভ করা
    output_file = "permanent_list.m3u8"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(m3u_content)
    
    print(f"✅ সফলভাবে {output_file} তৈরি হয়েছে! মোট চ্যানেল: {len(channels)}")

if __name__ == "__main__":
    generate_m3u()
