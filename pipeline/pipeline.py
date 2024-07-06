import asyncio
import concurrent.futures
from time import time
import ffmpeg
from TikTokApi import TikTokApi
from ffmpeg import Error
from yt_dlp import YoutubeDL
from asyncstdlib.itertools import islice
from pipeline.settings import *
from utils import generate_markdown_report


async def trending_videos(count=10):
    video_urls = []
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3)
        async for video in islice(api.trending.videos(count=count), 0, count):
            video_url = f"https://www.tiktok.com/@{video.author.username}/video/{video.id} "
            video_urls.append(video_url)
            print(f"Video: {video_url}"
                  f"Username: {video.author.username}"
                  f"Video ID: {video.id}")
    return video_urls


ydl_opts = {
    'quiet': True,
    'outtmpl': f'{output_folder}/%(uploader)s_%(id)s_%(timestamp)s.%(ext)s',
}


def download_video(video_url):
    ydl = YoutubeDL(ydl_opts)

    info_dict = ydl.extract_info(video_url, download=True)

    filename = ydl.prepare_filename(info_dict)
    return filename


def modify_video(video_path, audio_path):
    output_path = os.path.join(output_folder, f"temp_{os.path.basename(video_path)}")
    (
        ffmpeg
        .input(video_path)
        .filter('setpts', f'PTS/{speed_ratio_int}')
        .filter('scale', f'trunc(iw*{resize_ratio_int}/2)*2', f'trunc(ih*{resize_ratio_int}/2)*2')
        .output(output_path, vcodec='libx264', acodec='aac', preset='ultrafast')
        .global_args('-y')
        .run(overwrite_output=True, capture_stdout=True, capture_stderr=True)
    )

    video_part = ffmpeg.input(output_path)
    audio_part = ffmpeg.input(audio_path)
    (
        ffmpeg
        .output(audio_part.audio, video_part.video, video_path, shortest=None, vcodec='copy')
        .global_args('-y')
        .run(overwrite_output=True, capture_stdout=True, capture_stderr=True)
    )

    os.remove(output_path)


def process_videos(video_urls) -> tuple[int, list[Error | Exception]]:
    num_videos_processed = 0
    exceptions = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []

        for video_url in video_urls:
            future = executor.submit(download_video, video_url)
            futures.append(future)

        for future in concurrent.futures.as_completed(futures):
            try:
                file_name = future.result()
                modify_video(file_name, audio)
            except ffmpeg.Error as e:
                exceptions.append(e)
                print(f"FFmpeg error occurred: {e.stderr.decode('utf8')}")
            except Exception as e:
                exceptions.append(e)
                print(f"An unexpected error occurred: {e}")
            else:
                num_videos_processed += 1
    return num_videos_processed, exceptions


def tik_tok_trending(count):
    try:
        t1 = time()
        urls = asyncio.run(trending_videos(count))
        num_of_vid, exceptions = process_videos(urls)
        t2 = time()
        generate_markdown_report(num_of_vid, t2 - t1, exceptions, report)
        print("All videos have been downloaded and modified.")
        print(f'Executed in {(t2 - t1):.4f}s')
    except asyncio.CancelledError:
        print("Asyncio task was cancelled.")
    except Exception as e:
        print(f"An error occurred: {e}")
