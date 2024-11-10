from flask import Flask, render_template, request, send_file, jsonify, url_for
import os
import threading
import time
from dotenv import load_dotenv
import spotipy
import spotipy.oauth2 as oauth2
from function import find_and_download_songs

load_dotenv()

app = Flask(__name__)

# Variabel global untuk menyimpan status progres
progress_status = ""

# Fungsi untuk memperbarui status progres
def update_progress(status):
    global progress_status
    progress_status = status
    print(status)

# Inisialisasi klien Spotify
def get_spotify_client():
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    auth_manager = oauth2.SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    return spotipy.Spotify(auth_manager=auth_manager)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/status')
def status():
    return jsonify({"progress": progress_status})

@app.route('/convert', methods=['POST'])
def convert():
    track_uri = request.form['track_uri']
    if track_uri.find("https://open.spotify.com/track/") != -1:
        track_uri = track_uri.replace("https://open.spotify.com/track/", "")
    if '?' in track_uri:
        track_uri = track_uri.split('?')[0]

    try:
        spotify_client = get_spotify_client()
        track_info = spotify_client.track(track_uri)
        track_name = track_info['name']
        artist_name = track_info['artists'][0]['name']

        update_progress(f"Downloading track '{track_name}' by '{artist_name}'...")
        filename = find_and_download_songs(track_name, artist_name)
        update_progress(f"Track '{track_name}' by '{artist_name}' has been downloaded successfully!")

        download_url = url_for('download_file', filename=filename)
        return jsonify({"status": "success", "message": f"Track '{track_name}' has been downloaded successfully!", "download_url": download_url})
    except Exception as e:
        update_progress(f"Error: {e}")
        return jsonify({"status": "error", "message": str(e)})

def delayed_file_removal(filename, delay=10):
    time.sleep(delay)
    try:
        if os.path.exists(filename):
            os.remove(filename)
            print(f"File {filename} has been removed after {delay} seconds.")
        else:
            print(f"File {filename} does not exist.")
    except Exception as e:
        print(f"Error removing file {filename}: {e}")

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(os.getcwd(), filename)

    threading.Thread(target=delayed_file_removal, args=(file_path, 10)).start()

    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
