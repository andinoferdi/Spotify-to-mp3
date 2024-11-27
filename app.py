import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from yt_dlp import YoutubeDL
import subprocess

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def get_metadata(youtube_url):
    options = {
        'quiet': True,
        'no_warnings': True,
    }
    with YoutubeDL(options) as ydl:
        info = ydl.extract_info(youtube_url, download=False)
        return {
            'title': info.get('title', 'Unknown Title'),
            'artist': info.get('artist', 'Unknown Artist'),
            'album': info.get('album', 'Unknown Album'),
            'thumbnail': info.get('thumbnail', ''),
        }

def download_youtube_music_as_mp3(youtube_url):
    options = {
        'format': 'bestaudio/best',
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            },
        ],
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
    }

    with YoutubeDL(options) as ydl:
        info = ydl.extract_info(youtube_url, download=True)
        filename = os.path.basename(ydl.prepare_filename(info).replace('.webm', '.mp3'))
    
    reduced_volume_file = os.path.join(DOWNLOAD_FOLDER, f"reduced_{filename}")
    original_file = os.path.join(DOWNLOAD_FOLDER, filename)
    subprocess.run([
        'ffmpeg', '-i', original_file, '-filter:a', 'volume=-5dB', '-y', reduced_volume_file
    ])

    os.replace(reduced_volume_file, original_file)
    return filename

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/get_metadata", methods=["POST"])
def get_metadata_route():
    youtube_url = request.json.get("url")
    try:
        metadata = get_metadata(youtube_url)
        return jsonify(metadata)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/convert", methods=["POST"])
def convert_route():
    youtube_url = request.json.get("url")
    try:
        filename = download_youtube_music_as_mp3(youtube_url)
        return jsonify({"filename": filename})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/downloads/<filename>")
def downloads(filename):
    file_path = os.path.join(DOWNLOAD_FOLDER, filename)
    if os.path.isfile(file_path):
        return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True, mimetype='audio/mpeg')
    else:
        return "File not found", 404

if __name__ == "__main__":
    app.run(debug=True)
