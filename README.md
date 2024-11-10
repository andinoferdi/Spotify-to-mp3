
---

# Spotify to MP3 - Python

The simplest way to convert/download your Spotify tracks into MP3 files using Python 3.

## How To Use

This project is intended to be easy-to-use. However, there are some setup steps needed, like installing necessary packages. Please read the instructions carefully.

### 1. Clone the Repository

To clone this repository using Git, use:

```bash
git clone https://github.com/AndinoFerdiansah/spotify-to-mp3-python.git
```

If you're not familiar with Git, you can download the repository as a .zip file by clicking the "Code" button at the top of the GitHub page, then select "Download ZIP." Extract the contents of the .zip file.

Open a terminal and navigate to the folder:

```bash
cd spotify-to-mp3-python/
```

### 2. Installing Dependencies

We will install the dependencies using pip, Python's package manager. If you don’t have pip, follow this guide to install it.

To install the required packages, run:

```bash
pip install -r requirements.txt
```

If a requirements.txt file is not available, use this command to install packages individually:

```bash
pip install spotipy youtube_dl youtube_search yt_dlp ffprobe ffmpeg
```

### 3. Setting up Spotify

Go to the Spotify Developer Dashboard and log in. Once on the Dashboard, click the green "Create App" button. For "App name" and "App description," you can enter anything. Check both agreement boxes and click "Create."

Copy the Client ID and Client Secret fields from the app dashboard. You’ll need these for the script.

### 4. Getting Spotify Track URI

To get a track’s URI from Spotify:

1. Open Spotify and find the track you want to download.
2. Right-click the track, select "Share," and click "Copy Spotify URI."
3. The URI will look like this: spotify:track:4cOdK2wGLETKBW3PvgPWqT.
   Save the characters after spotify:track: (e.g., 4cOdK2wGLETKBW3PvgPWqT) for use in the script.

### 5. Running the Program

Run the script by executing the following command in your terminal:

```bash
python app.py
```

This will start a local Flask server. Open your browser and navigate to http://localhost:5000. Enter the Spotify track URI to start the download.

### Debugging

If you encounter an error related to ffprobe or ffmpeg, make sure they are installed and accessible in your system PATH. Refer to this solution for more details.
