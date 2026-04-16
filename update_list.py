import os

# কনফিগারেশন
TARGET_IP = "198.195.239.50"
TARGET_PORT = "8095"
BASE_URL = f"http://{TARGET_IP}:{TARGET_PORT}"

def generate_m3u():
    file_path = "smisp.txt"
    
    if not os.path.exists(file_path):
        print(f"❌ Error: {file_path} পাওয়া যায়নি!")
        return

    m3u_content = "#EXTM3U\n"
    channels_found = 0

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
            current_name = ""
            for line in lines:
                # লাইন থেকে name খুঁজে বের করা
                if 'name:' in line:
                    current_name = line.split('name:')[1].split(',')[0].strip().replace('"', '').replace("'", "")
                
                # লাইন থেকে slug খুঁজে বের করা এবং লিঙ্ক তৈরি করা
                if 'slug:' in line and current_name:
                    current_slug = line.split('slug:')[1].split(',')[0].strip().replace('"', '').replace("'", "").replace("}", "")
                    
                    # m3u ফরম্যাটে ডাটা যোগ করা
                    stream_url = f"{BASE_URL}/{current_slug}/index.m3u8"
                    m3u_content += f'#EXTINF:-1 tvg-id="{current_slug}" tvg-name="{current_name}" group-title="SM BDIX", {current_name}\n'
                    m3u_content += f'#EXTVLCOPT:http-referrer=http://{TARGET_IP}/\n'
                    m3u_content += f"{stream_url}\n"
                    
                    channels_found += 1
                    current_name = "" # নাম রিসেট করা পরের চ্যানেলের জন্য

    except Exception as e:
        print(f"❌ এরর: {e}")
        return

    if channels_found > 0:
        with open("permanent_list.m3u8", "w", encoding="utf-8") as f:
            f.write(m3u_content)
        print(f"✅ সফল! {channels_found}টি চ্যানেল দিয়ে permanent_list.m3u8 তৈরি হয়েছে।")
    else:
        print("❌ দুঃখিত, smisp.txt এর ভেতর থেকে কোনো চ্যানেল ডাটা রিড করা সম্ভব হয়নি।")

if __name__ == "__main__":
    generate_m3u()
