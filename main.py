import argparse
from dataclasses import dataclass
from pathlib import Path

from yt_dlp import YoutubeDL

@dataclass
class VideoData:
    title: str 
    url: str

archive_file_name = 'archive.txt'

def initialize_archive(file):
    file = Path(f'./{file}')
    if not file.exists():
        Path.touch(f'./{file}')

def download_audio_file(youtube_url:str, file_path:str, skip_archive:bool):
    # add 'logger' if needed
    options = {
        'format': 'bestaudio/best',  
        'outtmpl': f'{file_path}/%(title)s.%(ext)s',
        'postprocessors': [{  
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',  
        }],    
        'ignoreerrors': True,
        }
    
    if not skip_archive:
        options.update({'download_archive': archive_file_name})

    with YoutubeDL(options) as ydl:
        ydl.download([youtube_url])

def get_video_data(youtube_url: str) -> list[VideoData]:

    options = {
        'quiet': True,
        'extract_flat': True
    }

    with YoutubeDL(options) as ydl:
        info = ydl.extract_info(youtube_url, download=False)
        if 'entries' in info:
            # playlist
            videos = [VideoData(title=entry['title'], url=entry['url']) for entry in info['entries']]
        else:
            # single video
            videos = [VideoData(title=info['title'], url=info['webpage_url'])]
    return videos


def main(args):
    youtube_link = args.yt_link
    file_path = args.file_path
    skip_archive = args.skip_archive
    archive_file = args.archive_file

    video_data_list = get_video_data(youtube_link)

    if not skip_archive:
        initialize_archive(archive_file)
        

    for video_data in video_data_list:
        download_audio_file(video_data.url, file_path, skip_archive)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Youtube Downloader",
        description="""Downloads a Youtube playlist or video to a folder.
                    The playlist or video must be either public or unlisted to successfully download.
                    """,
    )
    parser.add_argument("yt_link", help="YouTube link to either a video or playlist.")
    parser.add_argument(
        "-f",
        "--file-path",
        default=None,
        help="Path to folder to download Youtube videos. Defaults to the current directory.",
    )
    parser.add_argument('--archive-file', default=archive_file_name)
    parser.add_argument('--skip-archive', action='store_true', help="Skip reading from archive file to detect duplicate downloads.")

    main(parser.parse_args())
