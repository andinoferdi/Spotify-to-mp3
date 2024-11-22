import os
from flask import Flask, render_template, request, send_from_directory
from yt_dlp import YoutubeDL
import subprocess

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

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

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        youtube_url = request.form["url"]
        try:
            filename = download_youtube_music_as_mp3(youtube_url)
            return render_template("index.html", filename=filename)
        except Exception as e:
            return f"An error occurred: {e}", 500
    return render_template("index.html")

@app.route("/downloads/<filename>")
def downloads(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
