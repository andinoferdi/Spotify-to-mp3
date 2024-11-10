from flask import Flask, render_template, request, jsonify, url_for, send_file
from services import get_track_info, find_and_download_songs, ProgressService
from function import setup_environment, clean_filename
import threading
import os
import time
import logging

# Inisialisasi Flask, ProgressService, dan environment
app = Flask(__name__)
progress_service = ProgressService()
setup_environment()

# Setup logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s', filename='app_errors.log')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/status')
def status():
    return jsonify({"progress": progress_service.get_status()})

@app.route('/convert', methods=['POST'])
def convert():
    track_uri = request.form['track_uri']
    try:
        # Logging untuk URI yang diterima
        logging.info(f"Received Spotify URI: {track_uri}")

        # Mendapatkan informasi lagu dari Spotify
        try:
            track_info = get_track_info(track_uri)
            logging.info(f"Track info retrieved: {track_info}")
        except Exception as e:
            logging.error(f"Spotify API Error: {e}")
            progress_service.update_status("Error: Gagal mendapatkan informasi dari Spotify. Pastikan URI benar dan coba lagi.")
            return jsonify({"status": "error", "message": "Gagal mendapatkan informasi dari Spotify. Pastikan URI benar dan coba lagi."})

        # Bersihkan nama file
        track_name = clean_filename(track_info['name'])
        artist_name = clean_filename(track_info['artist'])
        album_name = track_info.get('album')
        album_cover_url = track_info.get('album_cover_url')

        # Logging informasi lagu dan album
        logging.info(f"Track Name: {track_name}, Artist Name: {artist_name}, Album Name: {album_name}, Album Cover URL: {album_cover_url}")

        progress_service.update_status(f"Mengunduh track '{track_name}' oleh '{artist_name}' dari YouTube...")

        # Panggil layanan unduhan dari YouTube
        try:
            filename = find_and_download_songs(track_name, artist_name, progress_service, album_name, album_cover_url)
            logging.info(f"File downloaded and saved as: {filename}")
        except PermissionError:
            logging.error("File access error: File sedang digunakan atau terkunci.")
            progress_service.update_status("Error: File sedang digunakan atau terkunci.")
            return jsonify({"status": "error", "message": "File sedang digunakan atau terkunci. Coba lagi nanti."})
        except Exception as e:
            logging.error(f"YouTube Download Error: {e}")
            progress_service.update_status("Error: Gagal mengunduh file dari YouTube. Coba lagi nanti.")
            return jsonify({"status": "error", "message": "Gagal mengunduh file dari YouTube. Coba lagi nanti."})

        # Perbarui status jika unduhan berhasil
        progress_service.update_status(f"Track '{track_name}' oleh '{artist_name}' berhasil diunduh!")

        # Generate URL unduhan
        download_url = url_for('download_file', filename=filename)
        return jsonify({"status": "success", "message": f"Track '{track_name}' berhasil diunduh!", "download_url": download_url})
    except Exception as e:
        logging.error(f"General Error: {e}")
        progress_service.update_status("Error: Terjadi kesalahan yang tidak terduga.")
        return jsonify({"status": "error", "message": "Terjadi kesalahan yang tidak terduga. Coba lagi nanti."})

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(os.getcwd(), filename)
    response = send_file(file_path, as_attachment=True)

    threading.Thread(target=delayed_file_removal, args=(file_path, 5)).start()
    return response

def delayed_file_removal(filename, delay=5):
    time.sleep(delay)
    if os.path.exists(filename):
        try:
            os.remove(filename)
            logging.info(f"File {filename} has been removed after {delay} seconds.")
        except Exception as e:
            logging.error(f"File Deletion Error: {e}")

if __name__ == '__main__':
    app.run(debug=True)
