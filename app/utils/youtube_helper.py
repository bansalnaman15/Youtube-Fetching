from datetime import datetime
from croniter import croniter
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from tortoise.exceptions import IntegrityError
from app.db.videos import Videos
from app.utils.settings import settings


class YoutubeHelper:
    def __init__(self):
        self.api_keys = settings.YOUTUBE_API_KEYS.split(',')
        self.current_key_index = 0

    def get_current_api_key(self):
        return self.api_keys[self.current_key_index]

    async def fetch_data(self, search_key, cron_schedule):
        print(datetime.now(), "Fetching data now!", search_key, "Schedule:", cron_schedule)

        now = datetime.now()
        iter = croniter(cron_schedule, now)
        current_run = iter.get_prev(datetime)
        difference = iter.get_next(datetime) - current_run
        last_run = current_run - difference
        print(f"Fetching data for '{search_key}' since '{last_run}' till {current_run}")

        while self.current_key_index < len(self.api_keys):
            try:
                videos = call_youtube_api(search_key, last_run, current_run, self.get_current_api_key())
            except HttpError as e:
                if e.resp.status == 403 and 'quotaExceeded' in str(e):
                    print(f"Quota exceeded for API key {self.get_current_api_key()}. Trying next key...")
                else:
                    print("Error Occured:", e.error_details)
                print("Using the next API KEY!")
                self.current_key_index += 1

            else:
                await self.save_data(videos)
                break
        else:
            print("All API keys exhausted. Please add more API keys.")

    async def save_data(self, data):
        print(f"Inserting {len(data)} videos")

        for item in data:
            video = Videos(**item)
            try:
                await video.save()
            except IntegrityError:
                print(f"Video already exists in the database. Skipping.")

        print("Insertion completed.")


def call_youtube_api(search_key, since_time, till_time, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)

    request = youtube.search().list(
        q=search_key,
        part='snippet',
        type='video',
        publishedAfter=since_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
        maxResults=50
    )
    response = request.execute()
    videos = []
    for item in response['items']:
        video = {
            'video_id': item.get('id', {}).get('videoId'),
            'title': item.get('snippet', {}).get('title'),
            'description': item.get('snippet', {}).get('description'),
            'thumbnail_url': item.get('snippet', {}).get('thumbnails', {}).get('default', {}).get('url'),
            'uploader': item.get('snippet', {}).get('channelTitle'),
            'published_at': item.get('snippet', {}).get('publishedAt'),
        }
        videos.append(video)

    return videos
