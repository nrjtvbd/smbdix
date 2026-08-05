import os

# Configuration (আপডেট করা নতুন IP)
TARGET_IP = "103.165.93.31"
TARGET_PORT = "8095"
BASE_URL = f"http://{TARGET_IP}:{TARGET_PORT}"

def generate_m3u():
    # SM_BDIX_ISP.m3u theke pawa channel list
    # Format: (Name, Slug/URL, Group, Logo)
    channels = [
        ("TSports HD", "Tsports", "Sports", f"http://{TARGET_IP}/img/channels/tsports.jpg"),
        ("START SPORTS1", "bdixbd.net_t.me/tvhoichoi24/video", "Sports", f"http://{TARGET_IP}/img/channels/starsports1hd.png"),
        ("STAR SPORTS2", "StarSports2", "Sports", f"http://{TARGET_IP}/img/channels/starsports2hd.png"),
        ("STAR SPORTS SELECT1 HD", "StarSportsSelect1", "Sports", f"http://{TARGET_IP}/img/channels/star-sports-selected-1.jpg"),
        ("STAR SPORTS SELECT2 HD", "StarSportsSelect2", "Sports", f"http://{TARGET_IP}/img/channels/star-sports-selected-2.jpg"),
        ("SONY SPORTS 2 HD", "SonyTenSports2", "Sports", f"http://{TARGET_IP}/img/channels/sonySports2.png"),
        ("SONY SPORTS 5 HD", "SonyTenSports5", "Sports", f"http://{TARGET_IP}/img/channels/sonySports5.png"),
        ("EURO SPORTS HD", "Eurosport", "Sports", f"http://{TARGET_IP}/img/channels/euroSports.png"),
        ("WiLLoW", "WiLLow", "Sports", f"http://{TARGET_IP}/img/channels/willow.jpg"),
        ("PTV", "PTV-kutta/video", "Sports", f"http://{TARGET_IP}/img/channels/ptvsports.png"),
        ("NAGORIK", "nagorik", "Bangla", f"http://{TARGET_IP}/img/channels/nagoriktv.png"),
        ("SHOMOY TV HD", "bdixbd.net_somoytv/video", "News", f"http://{TARGET_IP}/img/channels/somoytv.png"),
        ("NEWS24 HD", "News24", "News", f"http://{TARGET_IP}/img/channels/news24.png"),
        ("CHANNEL 24", "Channel24", "News", f"http://{TARGET_IP}/img/channels/channel24.png"),
        ("ATN NEWS HD", "bdixbd.net_AtnNews/video", "News", f"http://{TARGET_IP}/img/channels/atnnews.png"),
        ("EKATTOR TV HD", "ekattor", "News", f"http://{TARGET_IP}/img/channels/ekattortv.png"),
        ("JAMUNA TV", "bdixbd.net_JamunaTV/video", "News", f"http://{TARGET_IP}/img/channels/jamunaTv.png"),
        ("ATN Bangla HD", "bdixbd.net_AtnNews/video", "Bangla", f"http://{TARGET_IP}/img/channels/atnbangla.png"),
        ("BANGLA VISION HD", "bdixbd.net_Enter10Bangla/video", "Bangla", f"http://{TARGET_IP}/img/channels/banglavision.png"),
        ("CHANNEL I HD", "bdixbd.net_channelihd/video", "Bangla", f"http://{TARGET_IP}/img/channels/channeli.png"),
        ("GTV HD", "bdixbd.net_gazitvhd/video", "Bangla", f"http://{TARGET_IP}/img/channels/gtv.png"),
        ("NTV HD", "bdixbd.net_NTV/video", "Bangla", f"http://{TARGET_IP}/img/channels/ntv.png"),
        ("Maasranga HD", "Maasranga", "Bangla", f"http://{TARGET_IP}/img/channels/maasranga.png"),
        ("STAR JALSHA HD", "bdixbd.net_StarJalshaHD/video", "Indian Bangla", f"http://{TARGET_IP}/img/channels/starjalshahd.png"),
        ("Jalsha Movies HD", "JalshaMovies", "Bangla", f"http://{TARGET_IP}/img/channels/jalshamovies.png"),
        ("ZEE BANGLA HD", "bdixbd.net_ZeeBanglaCinemaHD/video", "Indian Bangla", f"http://{TARGET_IP}/img/channels/zeebanglahd.png"),
        ("ZEE BANGLA CHINEMA HD", "ZeeBanglaCinema", "Indian Bangla", f"http://{TARGET_IP}/img/channels/zeebanglacinema.png"),
        ("COLOR BANGLA", "bdixbd.net_ColorsBanglaHD/video", "Indian Bangla", f"http://{TARGET_IP}/img/channels/colorsbanglahd.png"),
        ("SONY AATH", "sonyAath", "Indian Bangla", f"http://{TARGET_IP}/img/channels/sonyaath.png"), # updated slug case
        ("SONY MAX HD", "SonyMAX", "Hindi", f"http://{TARGET_IP}/img/channels/sonymaxhd.png"),
        ("SONY TV HD", "SonyTv", "Hindi", f"http://{TARGET_IP}/img/channels/sonytvhd.png"),
        ("STAR PLUS HD", "StarPlus", "Hindi", f"http://{TARGET_IP}/img/channels/starplus.png"),
        ("STAR GOLD HD", "StarGold", "Hindi", f"http://{TARGET_IP}/img/channels/starGold.png"),
        ("STAR MOVIES HD", "StarMovies", "Hindi", f"http://{TARGET_IP}/img/channels/starMovies.png"),
        ("ZEE TV HD", "ZeeTV", "Hindi", f"http://{TARGET_IP}/img/channels/zeetv.png"),
        ("ZEE CHINEMA HD", "ZeeCinema", "Hindi", f"http://{TARGET_IP}/img/channels/zeecinemahd.png"),
        ("COLOR CINEPLEX HD", "ColorsCineplex", "Hindi", f"http://{TARGET_IP}/img/channels/colorscineplex.png"),
        ("DISCOVERY HD", "Discovery", "Documentary", f"http://{TARGET_IP}/img/channels/discoveryhd.png"),
        ("NATIONAL GEOGRAPHIC HD", "NationalGeographic", "Documentary", f"http://{TARGET_IP}/img/channels/natgeohd.png"),
        ("ANIMAL PLANET HD", "AnimalPlanet", "Documentary", f"http://{TARGET_IP}/img/channels/animal-planet-hd-us.png"),
        ("CARTOON NETWORK HD", "CartoonNetwork", "Kids", f"http://{TARGET_IP}/img/channels/cartoonnetwork.png"),
        ("POGO", "pogo", "Kids", f"http://{TARGET_IP}/img/channels/pogo.png"),
        ("SANGEET BANGLA", "sangeetBangla", "Music", f"http://{TARGET_IP}/img/channels/sangeetBangla.jpg"),
        ("9X JALWA", "9XJalwa", "Music", f"http://{TARGET_IP}/img/channels/9xJalwa.png")
    ]

    m3u_content = "#EXTM3U\n"
    print("🚀 Permanent list update hoyeche...")

    for name, slug, group, logo in channels:
        # Check if slug is already a full path or needs formatting
        if ".m3u8" in slug:
            stream_url = f"{BASE_URL}/{slug}"
        else:
            stream_url = f"{BASE_URL}/{slug}/index.m3u8"
            
        m3u_content += f'#EXTINF:-1 tvg-id="{slug}" tvg-name="{name}" tvg-logo="{logo}" group-title="{group}", {name}\n'
        m3u_content += f'#EXTVLCOPT:http-referrer=http://{TARGET_IP}/\n'
        m3u_content += f"{stream_url}\n"

    with open("permanent_list.m3u8", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    
    print(f"✅ Safol bhabe {len(channels)} ti channel playlist-e add kora hoyeche.")

if __name__ == "__main__":
    generate_m3u()
