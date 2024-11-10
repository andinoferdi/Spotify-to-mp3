import yt_dlp
from youtube_search import YoutubeSearch

def find_and_download_songs(track_name, artist):
    # Modifikasi pencarian untuk mencari "only audio"
    text_to_search = f"{artist} - {track_name} only audio"
    print(f"Searching for {text_to_search} on YouTube...")
    
    best_url = None
    attempts_left = 10
    while attempts_left > 0:
        try:
            results_list = YoutubeSearch(text_to_search, max_results=5).to_dict()
            for result in results_list:
                title = result['title'].lower()
                
                # Memastikan video bukan video musik resmi (official music video) atau video dengan "mv"
                if "official music video" not in title and "mv" not in title and "lyrics" not in title:
                    best_url = "https://www.youtube.com{}".format(result['url_suffix'])
                    print(f"Found potential match: {title}")
                    break
            if best_url:
                break
        except IndexError:
            attempts_left -= 1
            print(f"No valid URLs found for {text_to_search}, trying again ({attempts_left} attempts left).")
    
    if best_url is None:
        print(f"No valid URLs found for {text_to_search}, skipping track.")
        return None

    # Mengunduh audio dari YouTube dan mengonversinya menjadi MP3
    print(f"Initiating download for {text_to_search}.")
    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio/best',
        'outtmpl': f'{track_name} - {artist}.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }, {
            'key': 'FFmpegMetadata',
        }]
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(best_url, download=True)

    filename = ydl.prepare_filename(info_dict).replace('.webm', '').replace('.m4a', '') + ".mp3"
    print(f"The downloaded file name is: {filename}")
    return filename
