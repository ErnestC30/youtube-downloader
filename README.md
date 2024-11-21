Download youtube videos by providing either a link to a playlist or an individual youtube link.
This currently only downloads the audio file in 'm4a' format.
Requires 'ffmpeg' to be installed to extract audio files.

Start up virtual environment:
env\scripts\activate.ps1

Download playlist
python main.py <youtube-playlist-link-url> -f <file-location>

Read options for CLI:
python main.py --help
