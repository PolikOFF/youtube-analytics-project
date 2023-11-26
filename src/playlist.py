import datetime
import isodate

from googleapiclient.discovery import build
import os

api_key: str = os.getenv('API_KEY_YOUTUBE')


class PlayList:
    """
    Класс для работы с плейлистом c сайта YouTube
    """
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        # Информация по плейлисту
        self.request_playlist = self.youtube.playlists().list(id=playlist_id,
                                                              part='contentDetails,snippet',
                                                              maxResults=50,).execute()
        self.title = self.request_playlist['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'
        # Информация по видео в плейлисте
        self.request_videos = self.youtube.playlistItems().list(playlistId=playlist_id,
                                                                part='contentDetails, snippet',
                                                                maxResults=50,).execute()
        # Айдишники всех видео в плейлисте
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.request_videos['items']]
        # Все видеоролики из плейлиста
        self.video_response_duration = self.youtube.videos().list(part='contentDetails,statistics',
                                                                  id=','.join(self.video_ids)
                                                                  ).execute()

    @property
    def total_duration(self):
        """Метод подсчета общего времени продолжительности плейлиста"""
        all_duration_time = datetime.timedelta()
        for video in self.video_response_duration['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            all_duration_time += datetime.timedelta(seconds=duration.total_seconds())
        return all_duration_time

    def show_best_video(self):
        """Метод для получения ссылки на видео, имеющего наибольшее количество лайков"""
        max_likes = 0
        likely_video_id = None
        for item in self.video_response_duration['items']:
            video_id = item['id']
            likes = int(item['statistics']['likeCount'])
            if likes > max_likes:
                max_likes = likes
                likely_video_id = video_id
        return 'https://youtu.be/' + likely_video_id
