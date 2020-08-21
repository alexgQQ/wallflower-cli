"""
application code for interacting with the Imgur API
"""

import os
import requests

from imgurpython import ImgurClient


class MyImgurClient:
    '''
    Class for client interaction with the Imgur API.
    This makes use of the python client library: https://github.com/Imgur/imgurpython
    '''
    def __init__(self):

        self.client_id = os.getenv('IMGUR_CLIENT_ID')
        self.client_secret = os.getenv('IMGUR_CLIENT_SECRET')
        self.access_token = os.getenv('IMGUR_ACCESS_TOKEN')
        self.refresh_token = os.getenv('IMGUR_REFRESH_TOKEN')

        # Note since access tokens expire after an hour,
        # only the refresh token is required (library handles autorefresh)
        self.client = ImgurClient(
            self.client_id, self.client_secret, self.access_token, self.refresh_token)

    def favorited_galleries(self):
        '''
        Generator to return images from favorited imgur albums.
        This is done in a synchronous manner by grabbing each albums detail data
        and yielding all the images from each.
        Imgur API References:
        - https://apidocs.imgur.com/?version=latest#a432a8e6-2ece-4544-bc7a-2999eb586f06
        - https://apidocs.imgur.com/?version=latest#f64e44be-8bf3-47bb-90d5-d1bf39c5e417
        '''
        for item in self.client.get_account_favorites('me'):
            url = f'https://api.imgur.com/3/gallery/album/{item.id}'
            response = requests.get(
                url, headers={'Authorization': f'Client-ID {self.client_id}'})
            data = response.json()
            for image in data['data']['images']:
                yield image