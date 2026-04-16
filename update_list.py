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

        # আপনার ফাইলের আসল ডাটা ফরম্যাট অনুযায়ী Regex
        # এটি { name: "Channel Name", slug: "ChannelSlug" } এই অংশগুলো খুঁজে নেবে
        channels = re.findall(r'name\s*:\s*["\'](.*?)["\']\s*,\s*slug\s*:\s*["\'](.*?)["\']', content)

        if not channels:
            print("❌ ফাইলের ভেতর থেকে চ্যানেলের তথ্য রিড করা যাচ্ছে না।")
            return

        m3u_content = "#EXTM3U\n"
        print(f"🚀 {len(channels)}টি চ্যানেল পাওয়া গেছে। প্লেলিস্ট তৈরি হচ্ছে...")

        for name, slug in channels:
            # m3u ফরম্যাট
            stream_url = f"{BASE_URL}/{slug}/index.m3u8"
            m3u_content += f'#EXTINF:-1 tvg-id="{slug}" tvg-name="{name}", {name}\n'
            m3u_content += f'#EXTVLCOPT:http-referrer=http://{TARGET_IP}/\n'
            m3u_content += f"{stream_url}\n"

        with open("permanent_list.m3u8", "w", encoding="utf-8") as f:
            f.write(m3u_content)
        
        print(f"✅ সফল! {len(channels)}টি চ্যানেল নিয়ে permanent_list.m3u8 তৈরি হয়েছে।")

    except Exception as e:
        print(f"❌ এরর: {e}")

if __name__ == "__main__":
    generate_m3u()
