import os
from googleapiclient.discovery import build
import json

api_key: str = os.getenv('API_KEY_YOUTUBE')
youtube = build('youtube', 'v3', developerKey = api_key)


class YouTubeChannelInfo:
    """Класс для обращения к YouTube"""
    api_key: str = os.getenv('API_KEY_YOUTUBE')
    youtube = build('youtube', 'v3', developerKey = api_key)


    @classmethod
    def get_channel_info(cls, channel_id):
        """Создает экземпляр класса для работы с информацией по id канала."""
        channel = cls.youtube.channels().list(id = channel_id, part = 'snippet,statistics').execute()
        return channel


class Channel:
    """Класс для ютуб - канала"""


    def __init__(self, channel_id):
        """
        Экземпляр инициализируется id канала.
        Дальше все данные будут подтягиваться по API.
        """
        self.channel_id = channel_id
        self.info = YouTubeChannelInfo.get_channel_info(channel_id)
        self.title = self.info['items'][0]['snippet']['title']
        self.description = self.info['items'][0]['snippet']['description']
        self.url = 'https://www.youtube.com/channel/' + self.info['items'][0]['id']
        self.sub = self.info['items'][0]['statistics']['subscriberCount']
        self.video_count = self.info['items'][0]['statistics']['videoCount']
        self.view_count = self.info['items'][0]['statistics']['viewCount']


    def print_info(self, channel_id) -> None:
        """Выводит в консоль информацию о канале."""
        channel_info = (youtube.channels()
                        .list(id = channel_id, part = 'snippet,statistics').execute())
        print(channel_info)


    @classmethod
    def get_service(cls):
        """Класс-метод возвращает объект для работы с YouTube API"""
        return cls


    def to_json(self, filename):
        """
        Создает словарь с данными атрибутов класса и сохраняет в json файл
        """
        info_channel_dict = {}
        info_channel_dict['title'] = self.title
        info_channel_dict['description'] = self.description
        info_channel_dict['url'] = self.url
        info_channel_dict['sub'] = self.sub
        info_channel_dict['video_count'] = self.video_count
        info_channel_dict['view_count'] = self.view_count
        with open(filename, 'w') as f:
            json.dump(info_channel_dict, f)
