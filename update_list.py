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

    # জাভাস্ক্রিপ্ট অবজেক্ট ফরম্যাট থেকে ডাটা বের করার জন্য উন্নত Regex
    # এটি { name: "...", slug: "..." } এবং {name:'...', slug:'...'} দুইটাই ধরবে
    pattern = r'name\s*:\s*["\'](.*?)["\']\s*,\s*slug\s*:\s*["\'](.*?)["\']'
    channels = re.findall(pattern, content)

    if not channels:
        # যদি উপরেরটি কাজ না করে, তবে শুধু ডাবল কোট দিয়ে চেষ্টা করবে
        pattern_v2 = r'name:\s*"([^"]+)",\s*slug:\s*"([^"]+)"'
        channels = re.findall(pattern_v2, content)

    if not channels:
        print("❌ কোনো চ্যানেল পাওয়া যায়নি। অনুগ্রহ করে নিশ্চিত করুন smisp.txt ফাইলটিতে 'name' এবং 'slug' এই শব্দগুলো আছে।")
        return

    m3u_content = "#EXTM3U\n"
    print(f"🚀 {len(channels)}টি চ্যানেল সনাক্ত করা হয়েছে। প্লেলিস্ট তৈরি হচ্ছে...")

    count = 0
    for name, slug in channels:
        # অপ্রয়োজনীয় স্পেস বা ক্যারেক্টার ক্লিন করা
        clean_name = name.strip()
        clean_slug = slug.strip()
        
        # m3u ফরম্যাট তৈরি
        stream_url = f"{BASE_URL}/{clean_slug}/index.m3u8"
        
        m3u_content += f'#EXTINF:-1 tvg-id="{clean_slug}" tvg-name="{clean_name}" group-title="SM BDIX", {clean_name}\n'
        m3u_content += f'#EXTVLCOPT:http-referrer=http://{TARGET_IP}/\n'
        m3u_content += f'#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\n'
        m3u_content += f"{stream_url}\n"
        count += 1

    # আউটপুট ফাইল সেভ করা
    output_file = "permanent_list.m3u8"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(m3u_content)
    
    print(f"✅ সফলভাবে {output_file} তৈরি হয়েছে! মোট চ্যানেল: {count}")

if __name__ == "__main__":
    generate_m3u()
