import os
import re

# Configuration
TARGET_IP = "103.165.93.31"
TARGET_PORT = "8095"
BASE_URL = f"http://{TARGET_IP}:{TARGET_PORT}"

def auto_detect_channels():
    channels = []
    
    # ১. smbdix.txt স্ক্যান করা
    if os.path.exists("smbdix.txt"):
        try:
            with open("smbdix.txt", "r", encoding="utf-8") as f:
                content = f.read()

            # HTML/JS থেকে 8095 পোর্টের সাথে যুক্ত স্লাগগুলো অটো এক্সট্র্যাক্ট করা
            # উদাহরণ: 8095/SonyTv/index.m3u8 অথবা /SonyTv/
            matches = re.findall(r'8095/([^/"\'\s]+)', content)
            if not matches:
                matches = re.findall(r'/([^/"\'\s]+)/index\.m3u8', content)

            unique_slugs = list(dict.fromkeys(matches)) # ডুপ্লিকেট বাদ দেওয়া

            for slug in unique_slugs:
                # স্লাগ থেকে অটো ক্লিন চ্যানেল নাম জেনারেট
                # e.g., sonyAath -> Sony Aath, StarSports1 -> Star Sports 1
                clean_name = re.sub(r'([a-z])([A-Z])', r'\1 \2', slug)
                clean_name = re.sub(r'([a-zA-Z]+)(\d+)', r'\1 \2', clean_name)
                clean_name = clean_name.replace('_', ' ').replace('-', ' ').title()
                
                channels.append((clean_name, slug, "General"))

            if channels:
                print(f"⚡ smbdix.txt থেকে {len(channels)} টি চ্যানেল অটো ক্যাচ করা হয়েছে।")
                return channels
        except Exception as e:
            print(f"Error reading smbdix.txt: {e}")

    # ২. ব্যাকআপ: যদি smbdix.txt এ কোনো ম্যাচ না পাওয়া যায়, তবে permanent_list.m3u8 থেকে ব্যাকআপ নেবে
    if os.path.exists("permanent_list.m3u8"):
        try:
            with open("permanent_list.m3u8", "r", encoding="utf-8") as f:
                lines = f.readlines()
                for i in range(len(lines)):
                    if lines[i].startswith("#EXTINF"):
                        name_match = re.search(r'tvg-name="([^"]+)"', lines[i])
                        group_match = re.search(r'group-title="([^"]+)"', lines[i])
                        
                        name = name_match.group(1) if name_match else "Channel"
                        group = group_match.group(1) if group_match else "General"
                        
                        if i + 2 < len(lines) and "http" in lines[i+2]:
                            stream_url = lines[i+2].strip()
                            slug_match = re.search(r'8095/([^/]+)', stream_url)
                            slug = slug_match.group(1) if slug_match else ""
                            if slug:
                                channels.append((name, slug, group))
            if channels:
                print(f"🔄 permanent_list.m3u8 থেকে {len(channels)} টি চ্যানেল এক্সট্র্যাক্ট করা হয়েছে।")
                return channels
        except Exception as e:
            print(f"Error reading permanent_list.m3u8: {e}")

    return channels

def generate_m3u():
    channels = auto_detect_channels()

    if not channels:
        print("❌ কোনো চ্যানেল পাওয়া যায়নি! ফাইল চেক করুন।")
        return

    m3u_content = "#EXTM3U\n"
    print(f"🚀 Processing {len(channels)} channels...")

    for name, slug, group in channels:
        if ".m3u8" in slug:
            stream_url = f"{BASE_URL}/{slug}"
        else:
            stream_url = f"{BASE_URL}/{slug}/index.m3u8"

        # অটোমেটিক লোগো লিংক জেনারেট
        clean_slug = slug.replace('/video', '').split('/')[0]
        logo_url = f"http://{TARGET_IP}/img/channels/{clean_slug.lower()}.png"

        m3u_content += f'#EXTINF:-1 tvg-id="{slug}" tvg-name="{name}" tvg-logo="{logo_url}" group-title="{group}", {name}\n'
        m3u_content += f'#EXTVLCOPT:http-referrer=http://{TARGET_IP}/\n'
        m3u_content += f"{stream_url}\n"

    # ফাইল আপডেট করা
    with open("permanent_list.m3u8", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    
    print(f"✅ Success! Updated permanent_list.m3u8 with {len(channels)} channels.")

if __name__ == "__main__":
    generate_m3u()
