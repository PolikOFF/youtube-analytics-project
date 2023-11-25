import os
from googleapiclient.discovery import build

api_key: str = os.getenv('API_KEY_YOUTUBE')


class Video:

    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id):
        self.video_id = video_id
        request = self.youtube.videos().list(part="snippet,contentDetails,statistics",
                                             id=video_id).execute()
        self.name = request['items'][0]['snippet']['title']
        self.url = 'https://www.youtube.com/watch?v=' + self.video_id
        self.watch_count = request['items'][0]['statistics']['viewCount']
        self.like_count = request['items'][0]['statistics']['likeCount']

    def __str__(self):
        return self.name


class PLVideo(Video):
    def __init__(self,video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

    def __str__(self):
        return self.name