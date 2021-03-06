"""
application code for interacting with the Reddit API
"""

import os
import praw

from funcy import compact
from app.config import supported_formats
from app.mongo import Wallpaper


class RedditClient:
    '''
    Class for client interaction with the Reddit API.
    This makes use of the python client library: https://praw.readthedocs.io/en/latest/
    '''

    source_type = 'reddit'

    def __init__(self, *args, **kwargs):

        client_id = os.getenv('REDDIT_CLIENT_ID')
        client_secret = os.getenv('REDDIT_CLIENT_SECRET')
        username = os.getenv('REDDIT_USERNAME')
        password = os.getenv('REDDIT_PASSWORD')
        user_agent = 'osx:wall-flower-cli:v0.0.1 (by /u/PocketBananna)'

        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            username=username,
            password=password,
            user_agent=user_agent
            )
        self.pagination = compact({
            'before': kwargs.get('before'),
            'after': kwargs.get('after'),
            'limit': kwargs.get('limit'),
        })

    def saved_wallpapers(self, limit: int = 500):
        '''
        Returns a generator of reddit Submissions for saved posts from r/wallpaper/
        can provide a limit of images to grab at once.
        '''
        for item in self.reddit.user.me().saved(limit=limit, params=self.pagination):
            if isinstance(item, praw.models.Submission) \
                and item.subreddit.display_name == 'wallpaper':
                    yield item

    @staticmethod
    def to_db(obj):

        ext = obj.url.split('.')[-1]
        found_frmt = [frmt in ext for frmt in supported_formats]
        if ext not in supported_formats and any(found_frmt):
            ext = supported_formats[found_frmt.index(True)]

        return {
            'url': obj.url,
            'source_id': obj.id,
            'extension': ext,
            'source_type': RedditClient.source_type,
            'active': ext in supported_formats,
        }

    def fetch(self, limit: int = 20):
        for wallpaper in self.saved_wallpapers(limit=limit):
            if getattr(wallpaper, 'is_gallery', False):
                for entry in wallpaper.gallery_data['items']:
                    image_id = entry['media_id']
                    ext = wallpaper.media_metadata[image_id]['m']
                    ext = ext.split('/')[-1]
                    wallpaper.url = f'https://i.redd.it/{image_id}.{ext}'
                    yield self.to_db(wallpaper)
            else:
                yield self.to_db(wallpaper)
