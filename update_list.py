import os

# Configuration
TARGET_IP = "198.195.239.50"
TARGET_PORT = "8095"
BASE_URL = f"http://{TARGET_IP}:{TARGET_PORT}"

def generate_m3u():
    # SM_BDIX_ISP.m3u theke pawa channel list
    # Format: (Name, Slug/URL, Group, Logo)
    channels = [
        ("TSports HD", "Tsports", "Sports", "http://198.195.239.50/img/channels/tsports.jpg"),
        ("START SPORTS1", "bdixbd.net_t.me/tvhoichoi24/video", "Sports", "http://198.195.239.50/img/channels/starsports1hd.png"),
        ("STAR SPORTS2", "StarSports2", "Sports", "http://198.195.239.50/img/channels/starsports2hd.png"),
        ("STAR SPORTS SELECT1 HD", "StarSportsSelect1", "Sports", "http://198.195.239.50/img/channels/star-sports-selected-1.jpg"),
        ("STAR SPORTS SELECT2 HD", "StarSportsSelect2", "Sports", "http://198.195.239.50/img/channels/star-sports-selected-2.jpg"),
        ("SONY SPORTS 2 HD", "SonyTenSports2", "Sports", "http://198.195.239.50/img/channels/sonySports2.png"),
        ("SONY SPORTS 5 HD", "SonyTenSports5", "Sports", "http://198.195.239.50/img/channels/sonySports5.png"),
        ("EURO SPORTS HD", "Eurosport", "Sports", "http://198.195.239.50/img/channels/euroSports.png"),
        ("WiLLoW", "WiLLow", "Sports", "http://198.195.239.50/img/channels/willow.jpg"),
        ("PTV", "PTV-kutta/video", "Sports", "http://198.195.239.50/img/channels/ptvsports.png"),
        ("NAGORIK", "nagorik", "Bangla", "http://198.195.239.50/img/channels/nagoriktv.png"),
        ("SHOMOY TV HD", "bdixbd.net_somoytv/video", "News", "http://198.195.239.50/img/channels/somoytv.png"),
        ("NEWS24 HD", "News24", "News", "http://198.195.239.50/img/channels/news24.png"),
        ("CHANNEL 24", "Channel24", "News", "http://198.195.239.50/img/channels/channel24.png"),
        ("ATN NEWS HD", "bdixbd.net_AtnNews/video", "News", "http://198.195.239.50/img/channels/atnnews.png"),
        ("EKATTOR TV HD", "ekattor", "News", "http://198.195.239.50/img/channels/ekattortv.png"),
        ("JAMUNA TV", "bdixbd.net_JamunaTV/video", "News", "http://198.195.239.50/img/channels/jamunaTv.png"),
        ("ATN Bangla HD", "bdixbd.net_AtnNews/video", "Bangla", "http://198.195.239.50/img/channels/atnbangla.png"),
        ("BANGLA VISION HD", "bdixbd.net_Enter10Bangla/video", "Bangla", "http://198.195.239.50/img/channels/banglavision.png"),
        ("CHANNEL I HD", "bdixbd.net_channelihd/video", "Bangla", "http://198.195.239.50/img/channels/channeli.png"),
        ("GTV HD", "bdixbd.net_gazitvhd/video", "Bangla", "http://198.195.239.50/img/channels/gtv.png"),
        ("NTV HD", "bdixbd.net_NTV/video", "Bangla", "http://198.195.239.50/img/channels/ntv.png"),
        ("Maasranga HD", "Maasranga", "Bangla", "http://198.195.239.50/img/channels/maasranga.png"),
        ("STAR JALSHA HD", "bdixbd.net_StarJalshaHD/video", "Indian Bangla", "http://198.195.239.50/img/channels/starjalshahd.png"),
        ("Jalsha Movies HD", "JalshaMovies", "Bangla", "http://198.195.239.50/img/channels/jalshamovies.png"),
        ("ZEE BANGLA HD", "bdixbd.net_ZeeBanglaCinemaHD/video", "Indian Bangla", "http://198.195.239.50/img/channels/zeebanglahd.png"),
        ("ZEE BANGLA CHINEMA HD", "ZeeBanglaCinema", "Indian Bangla", "http://198.195.239.50/img/channels/zeebanglacinema.png"),
        ("COLOR BANGLA", "bdixbd.net_ColorsBanglaHD/video", "Indian Bangla", "http://198.195.239.50/img/channels/colorsbanglahd.png"),
        ("SONY AATH", "SonyAath", "Indian Bangla", "http://198.195.239.50/img/channels/sonyaath.png"),
        ("SONY MAX HD", "SonyMAX", "Hindi", "http://198.195.239.50/img/channels/sonymaxhd.png"),
        ("SONY TV HD", "SonyTv", "Hindi", "http://198.195.239.50/img/channels/sonytvhd.png"),
        ("STAR PLUS HD", "StarPlus", "Hindi", "http://198.195.239.50/img/channels/starplus.png"),
        ("STAR GOLD HD", "StarGold", "Hindi", "http://198.195.239.50/img/channels/starGold.png"),
        ("STAR MOVIES HD", "StarMovies", "Hindi", "http://198.195.239.50/img/channels/starMovies.png"),
        ("ZEE TV HD", "ZeeTV", "Hindi", "http://198.195.239.50/img/channels/zeetv.png"),
        ("ZEE CHINEMA HD", "ZeeCinema", "Hindi", "http://198.195.239.50/img/channels/zeecinemahd.png"),
        ("COLOR CINEPLEX HD", "ColorsCineplex", "Hindi", "http://198.195.239.50/img/channels/colorscineplex.png"),
        ("DISCOVERY HD", "Discovery", "Documentary", "http://198.195.239.50/img/channels/discoveryhd.png"),
        ("NATIONAL GEOGRAPHIC HD", "NationalGeographic", "Documentary", "http://198.195.239.50/img/channels/natgeohd.png"),
        ("ANIMAL PLANET HD", "AnimalPlanet", "Documentary", "http://198.195.239.50/img/channels/animal-planet-hd-us.png"),
        ("CARTOON NETWORK HD", "CartoonNetwork", "Kids", "http://198.195.239.50/img/channels/cartoonnetwork.png"),
        ("POGO", "pogo", "Kids", "http://198.195.239.50/img/channels/pogo.png"),
        ("SANGEET BANGLA", "sangeetBangla", "Music", "http://198.195.239.50/img/channels/sangeetBangla.jpg"),
        ("9X JALWA", "9XJalwa", "Music", "http://198.195.239.50/img/channels/9xJalwa.png")
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
