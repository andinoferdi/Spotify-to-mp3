import yt_dlp
from youtube_search import YoutubeSearch
import os
import requests
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, APIC, error

def find_and_download_songs(track_name, artist, progress_service, album=None, album_cover_url=None):
    text_to_search = f"{artist} - {track_name} only audio"
    best_url = None

    # Coba cari di YouTube
    results_list = YoutubeSearch(text_to_search, max_results=5).to_dict()
    for result in results_list:
        title = result['title'].lower()
        if all(exclude not in title for exclude in ["official music video", "mv", "lyrics"]):
            best_url = "https://www.youtube.com{}".format(result['url_suffix'])
            break

    if not best_url:
        raise Exception(f"No valid URLs found for {text_to_search}")

    # Unduh audio
    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio/best',
        'outtmpl': f'{track_name}.temp.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }, {
            'key': 'FFmpegMetadata',
        }]
    }

    progress_service.update_status("Downloading from YouTube...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(best_url, download=True)

    temp_filename = ydl.prepare_filename(info_dict).replace('.webm', '').replace('.m4a', '') + ".mp3"
    final_filename = f"{track_name}.mp3"
    os.rename(temp_filename, final_filename)

    # Menambahkan metadata ke file MP3
    add_metadata_to_mp3(final_filename, track_name, artist, album, album_cover_url)

    return final_filename

def add_metadata_to_mp3(filename, track_name, artist, album, album_cover_url):
    """Menambahkan metadata seperti judul lagu, artis, album, dan gambar album ke file MP3."""
    try:
        # Tambahkan metadata dasar
        audio = MP3(filename, ID3=ID3)
        try:
            audio.add_tags()
        except error:
            pass  # Jika tag sudah ada, lanjutkan

        audio.tags["TIT2"] = TIT2(encoding=3, text=track_name)  # Judul lagu
        audio.tags["TPE1"] = TPE1(encoding=3, text=artist)  # Artis
        audio.tags["TALB"] = TALB(encoding=3, text=album if album else "Unknown Album")  # Album

        # Unduh gambar album dan tambahkan sebagai cover art
        if album_cover_url:
            response = requests.get(album_cover_url)
            if response.status_code == 200:
                print("Album cover downloaded successfully.")
                mime_type = 'image/jpeg' if album_cover_url.endswith('.jpg') or album_cover_url.endswith('.jpeg') else 'image/png'
                audio.tags.add(
                    APIC(
                        encoding=3,        # UTF-8 encoding
                        mime=mime_type,    # MIME type for the image
                        type=3,            # 3 is for the album front cover
                        desc='Cover',
                        data=response.content
                    )
                )
                print("Album cover added to metadata.")
            else:
                print("Failed to download album cover.")
        else:
            print("No album cover URL provided.")

        audio.save()
        print(f"Metadata added to {filename}")
    except Exception as e:
        print(f"Error adding metadata: {e}")
