import os
import spotipy
import spotipy.oauth2 as oauth2
import yt_dlp
from youtube_search import YoutubeSearch
import urllib.request
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error
import time  # Importing time for adding delays

def write_track(text_file: str, track: dict):
    # Write the track information to a file
    with open(text_file, 'w+', encoding='utf-8') as file_out:
        try:
            track_url = track['external_urls']['spotify']
            track_name = track['name']
            track_artist = track['artists'][0]['name']
            album_art_url = track['album']['images'][0]['url']
            csv_line = track_name + "," + track_artist + "," + track_url + "," + album_art_url + "\n"
            try:
                file_out.write(csv_line)
            except UnicodeEncodeError:  # Most likely caused by non-English song names
                print("Track named {} failed due to an encoding error. This is most likely due to this song having a non-English name.".format(track_name))
        except KeyError:
            print(u'Skipping track {0} by {1} (local only?)'.format(track['name'], track['artists'][0]['name']))

def write_single_track(username: str, track_id: str):
    results = spotify.track(track_id)
    track_name = results['name']
    text_file = u'{0}.txt'.format(track_name, ok='-_()[]{}')
    print(u'Writing track {0} to {1}.'.format(results['name'], text_file))
    write_track(text_file, results)
    return track_name, [results['album']['images'][0]['url']]

def find_and_download_songs(reference_file: str):
    TOTAL_ATTEMPTS = 10
    with open(reference_file, "r", encoding='utf-8') as file:
        for line in file:
            temp = line.split(",")
            name, artist, album_art_url = temp[0], temp[1], temp[3]
            text_to_search = artist + " - " + name
            best_url = None
            attempts_left = TOTAL_ATTEMPTS
            while attempts_left > 0:
                try:
                    results_list = YoutubeSearch(text_to_search, max_results=1).to_dict()
                    best_url = "https://www.youtube.com{}".format(results_list[0]['url_suffix'])
                    break
                except IndexError:
                    attempts_left -= 1
                    print("No valid URLs found for {}, trying again ({} attempts left).".format(text_to_search, attempts_left))
            if best_url is None:
                print("No valid URLs found for {}, skipping track.".format(text_to_search))
                continue

            print("Initiating download for Image {}.".format(album_art_url))
            f = open('{}.jpg'.format(name),'wb')
            f.write(urllib.request.urlopen(album_art_url).read())
            f.close()

            # Run yt-dlp to fetch and download the link's audio
            print("Initiating download for {}.".format(text_to_search))
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': '%(title)s.%(ext)s',  # Ensure the file extension is included
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

            # extract the name of the downloaded file from the info_dict
            filename = ydl.prepare_filename(info_dict).replace('.webm', '').replace('.m4a', '')
            print(f"The downloaded file name is: {filename}")

            print('AddingCoverImage ...')

            # Wait for the file to be accessible
            time.sleep(5)  # Add delay to ensure the file is ready

            audio = MP3(f'{filename}.mp3', ID3=ID3)
            try:
                audio.add_tags()
            except error:
                pass

            audio.tags.add(
                APIC(
                    encoding=3,  # 3 is for utf-8
                    mime="image/jpeg",  # can be image/jpeg or image/png
                    type=3,  # 3 is for the cover image
                    desc='Cover',
                    data=open(f'{name}.jpg', mode='rb').read()
                )
            )
            audio.save()
            os.remove(f'{name}.jpg')

if __name__ == "__main__":
    # Parameters
    print("Please read README.md for use instructions.")
    if os.path.isfile('config.ini'):
        import configparser
        config = configparser.ConfigParser()
        config.read("config.ini")
        client_id = config["Settings"]["client_id"]
        client_secret = config["Settings"]["client_secret"]
        username = config["Settings"]["username"]
    else:
        client_id = input("Client ID: ")
        client_secret = input("Client secret: ")
        username = input("Spotify username: ")
    track_uri = input("Track URI/Link: ")
    if track_uri.find("https://open.spotify.com/track/") != -1:
        track_uri = track_uri.replace("https://open.spotify.com/track/", "")
    if '?' in track_uri:
        track_uri = track_uri.split('?')[0]
    if len(track_uri) != 22 or not track_uri.isalnum():
        raise ValueError("Invalid Track ID")
    print(f"Username: {username}, Track ID: {track_uri}")
    auth_manager = oauth2.SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    track_name, albumArtUrls = write_single_track(username, track_uri)
    reference_file = "{}.txt".format(track_name)
    # Create the track folder
    if not os.path.exists(track_name):
        os.makedirs(track_name)
    os.rename(reference_file, track_name + "/" + reference_file)
    os.chdir(track_name)
    find_and_download_songs(reference_file)
    os.remove(f'{reference_file}')
    print("Operation complete.")
