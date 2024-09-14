import instaloader
import os
import glob
import shutil
import requests
import yt_dlp
import os
import requests
from bs4 import BeautifulSoup


async def download_media_from_instagram(url, user_id):
    try:
        loader = instaloader.Instaloader()
        loader.login(user="telebotsnowayrm", passwd="0960908006Roman")
        if loader.login:
            print("12")
        shortcode = extract_shortcode(url)
        if not shortcode:
            print("Invalid Instagram URL")
            return None
        post = instaloader.Post.from_shortcode(loader.context, shortcode)

        # Define the directory to save the downloaded media with user_id as directory name
        save_dir = f"instagram_downloads_{user_id}"
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # Download the post to the save directory
        loader.download_post(post, target=save_dir)

        # Get all media files in the directory
        all_files = glob.glob(os.path.join(save_dir, "*"))

        # Filter out only valid media files and exclude video cover images
        media_files = []
        for file in all_files:
            if file.endswith(".mp4"):
                media_files.append(file)  # Add only video files
            elif file.endswith(('.jpg', '.jpeg', '.png')):
                # Add only images if the post is not a video
                if not post.is_video:
                    media_files.append(file)

        if not media_files:
            print(f"No valid media files found in directory: {save_dir}")
            return None

        # Limit media to 10 files if there are more than 10
        media_files = media_files[:10]

        return {
            'files': media_files,
            'dir': save_dir,
            'caption': post.caption,
            'is_video': post.is_video
        }

    except Exception as e:
        print(f"Error downloading Instagram media: {e}")
        return None


def extract_shortcode(url):
    if "instagram.com/p/" in url:
        return url.split("/p/")[1].split("/")[0]
    elif "instagram.com/reel/" in url:
        return url.split("/reel/")[1].split("/")[0]


async def download_media_from_tiktok(media_url, user_id):
    try:
        # Настройки для yt-dlp
        ydl_opts = {
            'format': 'best',
            'outtmpl': f'tiktok_downloads_{user_id}/%(id)s.%(ext)s',
            'noplaylist': True,  # Не загружать плейлисты
            'quiet': True,  # Без вывода лога
            'writeinfojson': True,  # Записывает метаданные в формате JSON
        }

        # Создаем директорию для сохранения видео
        save_dir = f"tiktok_downloads_{user_id}"
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # Загружаем видео
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(media_url, download=True)
            video_path = os.path.join(save_dir, f"{info_dict['id']}.mp4")
            title = info_dict.get('title', '')

        return {
            'files': [video_path],
            'dir': save_dir,
            'caption': title  # Используем описание или заголовок как подпись
        }

    except Exception as e:
        print(f"Error downloading TikTok media: {e}")
        return None




import os
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError as YoutubeDLError
from os.path import join
from typing import Optional, Dict

TEMP_DIR = 'youtube_shorts_downloads'

class VideoDownloader:
    @staticmethod
    def _remove_unwanted_chars(string: str) -> str:
        return ''.join(e for e in string if e.isalnum() or e in (' ', '-', '_')).rstrip()

    async def download_media_from_youtube_shorts(self, media_url: str, user_id: str) -> Optional[Dict]:
        """
        Downloads YouTube Shorts video and returns media information.

        Args:
            media_url (str): URL of the YouTube Shorts video.
            user_id (str): ID of the user requesting the download.

        Returns:
            Optional[Dict]: Information about downloaded media, or None if the download failed.
        """
        options: dict = {
            "format": "best",
            "geo_bypass": True,
            "noplaylist": True,
            "noprogress": True,
            "quiet": True,
        }
        ydl: YoutubeDL = YoutubeDL(params=options)

        try:
            # Get information about the video
            video_info = ydl.extract_info(media_url, download=False)
            duration: Optional[int] = video_info.get("duration")

            if duration and duration <= 60:
                # Set save folder and file name
                title: str = video_info.get("title")
                save_dir = f"youtube_shorts_downloads_{user_id}"
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)
                
                path_to_file: str = join(save_dir, f"{self._remove_unwanted_chars(string=title)}.mp4")
                params: dict = getattr(ydl, "params")
                params.update({"outtmpl": {"default": path_to_file}})
                setattr(ydl, "params", params)

                # Download the video
                ydl.download([media_url])

                return {
                    'files': [path_to_file],
                    'dir': save_dir,
                    'caption': title
                }

        except YoutubeDLError as ex:
            print(f"Error when loading video: {repr(ex)}")

        return None


async def download_media_from_twitter(media_url):
    # Logic for downloading from Twitter
    return {'type': 'photo', 'file': 'path_to_twitter_photo.jpg'}


async def download_media_from_pinterest(media_url, user_id):
    response = requests.get(media_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    media_files = []
    save_dir = f"downloads/{user_id}"
    os.makedirs(save_dir, exist_ok=True)

    img_tag = soup.find('img', {'class': 'hCL kVc L4E MIw'})
    if img_tag:
        img_url = img_tag['src']
        img_response = requests.get(img_url)
        img_path = os.path.join(save_dir, f"{user_id}_pinterest_image.jpg")
        with open(img_path, 'wb') as img_file:
            img_file.write(img_response.content)
        media_files.append(img_path)

    video_tag = soup.find('video', {'class': 'some-video-class'})
    if video_tag:
        video_url = video_tag['src']
        video_response = requests.get(video_url)
        video_path = os.path.join(save_dir, f"{user_id}_pinterest_video.mp4")
        with open(video_path, 'wb') as video_file:
            video_file.write(video_response.content)
        media_files.append(video_path)

    return {
        'files': media_files,
        'dir': save_dir,
        'caption': '',  # Add caption if needed
        'is_video': False  # Change to True if video is found
    }
