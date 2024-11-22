
# Spotify-to-MP3 Converter Web Application

A simple Flask web application to convert YouTube Music links to MP3 with reduced volume. The application processes the files on the server, allowing users to download the adjusted MP3 directly.

## Features
- Converts YouTube Music links to MP3 format.
- Reduces the MP3 volume by -5 dB.
- No local storage — processed files are streamed directly to the user.

---

## Prerequisites
Before you begin, ensure you have the following installed on your system:

1. **Python 3.10+**
2. **FFmpeg** (for audio processing)
3. **pip** (Python package installer)

---

## Getting Started

Follow these steps to clone and run the project:

### 1. Clone the Repository
Run the following commands to clone the repository and navigate to the project folder:
```bash
git clone https://github.com/andinoferdi/YoutubeMusic-to-mp3
```

### 2. Set Up a Virtual Environment
Setting up a virtual environment helps manage dependencies and avoid conflicts with other Python projects. Follow these steps:

- **For Linux/Mac**:
  1. Run `python -m venv venv` to create a virtual environment.
  2. Activate the virtual environment by running `source venv/bin/activate`.

- **For Windows**:
  1. Run `python -m venv venv` to create a virtual environment.
  2. Activate the virtual environment by running `venv\Scripts\activate`.

After activating the virtual environment, your terminal prompt will indicate that you're inside the virtual environment.

### 3. Install Dependencies
Install the required Python libraries by running:
```bash
pip install -r requirements.txt
```

### 4. Install FFmpeg
Ensure FFmpeg is installed and accessible via your system's PATH.

- **Linux (Ubuntu/Debian)**:
  ```bash
  sudo apt update
  sudo apt install ffmpeg
  ```
- **Mac**:
  ```bash
  brew install ffmpeg
  ```
- **Windows**:
  - Download FFmpeg from [FFmpeg.org](https://ffmpeg.org/download.html).
  - Add the FFmpeg `bin` folder to your system's PATH.

### 5. Run the Application
Start the Flask application by running:
```bash
python app.py
```

### 6. Access the Web App
Open your web browser and navigate to:
```
http://127.0.0.1:5000/
```

---

## How to Use
1. Enter a valid YouTube Music link in the text input field.
2. Click **"Convert & Download"**.
3. The server will process the link and return a downloadable MP3 file.

---

## Project Structure
```
project/
├── app.py            # Main Flask application
├── templates/
│   ├── index.html    # HTML for the web interface
├── static/
│   ├── style.css     # CSS for the web interface
```

---

## Requirements
```
Flask==2.3.3
yt-dlp==2023.10.22
```

Install them using:
```bash
pip install -r requirements.txt
```

---

## Notes
- Ensure your internet connection is stable when downloading from YouTube Music.
- All file processing is done in-memory; no files are stored locally.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
