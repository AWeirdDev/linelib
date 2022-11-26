import requests

from ..const import DEFAULT

api = DEFAULT.api

def get_user(CAT: str, user_id: str):
    """
    Fetch a user. Returns a `User` object.

    :param str CAT: Channel access token.
    :param str user_id: The user id.
    """
    r = requests.get(api + "/profile/" + user_id, headers={
        "Authorization": "Bearer " + CAT
    })
    
    class User:
        def __init__(self, json):
            self.json = json
            
        @property
        def name(self):
            return self.json['displayName']

        displayName = name
        
        @property
        def user_id(self):
            return self.json['userId']

        userId = id = user_id

        @property
        def language(self):
            return self.json['language']

        @property
        def avatar_url(self):
            return self.json['pictureUrl']

        picture = pictureUrl = pictureURL = avatarUrl = avatarURL = avatar_url

        @property
        def status(self):
            if not "statusMessage" in self.json:
                return None
            else:
                return self.json['statusMessage']

        status_message = statusMessage = status

        @property
        def id(self):
            return user_id
        
    return User(r.json())
