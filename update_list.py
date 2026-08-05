import os
import re

# Configuration
TARGET_IP = "103.165.93.31"
TARGET_PORT = "8095"
BASE_URL = f"http://{TARGET_IP}:{TARGET_PORT}"

def auto_generate_slug(channel_name):
    """
    যেকোনো চ্যানেল নেম থেকে সম্পূর্ণ অটোমেটিক সার্ভার স্লগ জেনারেট করার ফাংশন।
    উদাহরণ: 
    - "SONY AATH" -> "sonyAath"
    - "STAR SPORTS 2" -> "StarSports2"
    - "CHANNEL 24" -> "Channel24"
    """
    # স্পেশাল ক্যারেক্টার ও সিম্বল পরিষ্কার করা
    clean_name = re.sub(r'[^a-zA-Z0-9\s]', '', channel_name)
    words = clean_name.split()

    if not words:
        return channel_name.lower()

    # প্রথম শব্দটি ছোট হাতের এবং পরের শব্দগুলো বড় হাতের (camelCase)
    # অথবা সার্ভারের স্ট্যান্ডার্ড অনুযায়ী শব্দগুলো সাজানো
    if len(words) == 1:
        # যেমন: "nagorik" -> "nagorik" বা "Ekattor"
        return words[0].lower() if words[0].isupper() else words[0]
    
    # একাধিক শব্দ থাকলে প্রথমটি ছোট/ক্যাপ্স এবং পরেরটি CamelCase
    # যেমন: SONY AATH -> sonyAath
    first_word = words[0].lower()
    remaining_words = "".join(w.capitalize() for w in words[1:])
    
    return f"{first_word}{remaining_words}"

def generate_m3u():
    # সম্পূর্ণ সাধারণ লিস্ট (কোথাও কোনো ম্যানুয়াল স্লগ বা লিংক নেই)
    channels = [
        ("TSports HD", "Sports"),
        ("START SPORTS1", "Sports"),
        ("STAR SPORTS2", "Sports"),
        ("STAR SPORTS SELECT1 HD", "Sports"),
        ("STAR SPORTS SELECT2 HD", "Sports"),
        ("SONY SPORTS 2 HD", "Sports"),
        ("SONY SPORTS 5 HD", "Sports"),
        ("EURO SPORTS HD", "Sports"),
        ("WiLLoW", "Sports"),
        ("PTV", "Sports"),
        ("NAGORIK", "Bangla"),
        ("SHOMOY TV HD", "News"),
        ("NEWS24 HD", "News"),
        ("CHANNEL 24", "News"),
        ("ATN NEWS HD", "News"),
        ("EKATTOR TV HD", "News"),
        ("JAMUNA TV", "News"),
        ("ATN Bangla HD", "Bangla"),
        ("BANGLA VISION HD", "Bangla"),
        ("CHANNEL I HD", "Bangla"),
        ("GTV HD", "Bangla"),
        ("NTV HD", "Bangla"),
        ("Maasranga HD", "Bangla"),
        ("STAR JALSHA HD", "Indian Bangla"),
        ("Jalsha Movies HD", "Bangla"),
        ("ZEE BANGLA HD", "Indian Bangla"),
        ("ZEE BANGLA CHINEMA HD", "Indian Bangla"),
        ("COLOR BANGLA", "Indian Bangla"),
        ("SONY AATH", "Indian Bangla"),
        ("SONY MAX HD", "Hindi"),
        ("SONY TV HD", "Hindi"),
        ("STAR PLUS HD", "Hindi"),
        ("STAR GOLD HD", "Hindi"),
        ("STAR MOVIES HD", "Hindi"),
        ("ZEE TV HD", "Hindi"),
        ("ZEE CHINEMA HD", "Hindi"),
        ("COLOR CINEPLEX HD", "Hindi"),
        ("DISCOVERY HD", "Documentary"),
        ("NATIONAL GEOGRAPHIC HD", "Documentary"),
        ("ANIMAL PLANET HD", "Documentary"),
        ("CARTOON NETWORK HD", "Kids"),
        ("POGO", "Kids"),
        ("SANGEET BANGLA", "Music"),
        ("9X JALWA", "Music")
    ]

    m3u_content = "#EXTM3U\n"
    print("🚀 Auto-mapping playlist generation shuru hocche...")

    for name, group in channels:
        # ১০০% অটোমেটিক স্লগ তৈরি
        slug = auto_generate_slug(name)
        stream_url = f"{BASE_URL}/{slug}/index.m3u8"
        logo_url = f"http://{TARGET_IP}/img/channels/{slug.lower()}.png"

        m3u_content += f'#EXTINF:-1 tvg-id="{slug}" tvg-name="{name}" tvg-logo="{logo_url}" group-title="{group}", {name}\n'
        m3u_content += f'#EXTVLCOPT:http-referrer=http://{TARGET_IP}/\n'
        m3u_content += f"{stream_url}\n"

    with open("permanent_list.m3u8", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    
    print(f"✅ Safol bhabe {len(channels)} ti channel automatic process hoye playlist-e add hoyeche.")

if __name__ == "__main__":
    generate_m3u()
