import requests, datetime
from typing import List, Union
from .new import TextMessage

from ..const import DEFAULT
from ..errors import AlreadyHandled, lineApiError

api = DEFAULT.api

class _WebhookEvent(object):
    def __init__(self, e):
        self.event_id = self.eventId = e['webhookEventId']
        self.isRedelivery = e['deliveryContext']['isRedelivery']

class WM():
    handled = False
    def reply(self, messages: List[Union[TextMessage]]):
        if self.handled:
            raise AlreadyHandled("\n\nAnother handler has already handled this event, or you're trying to send a message twice or more. If so, you could use an Array (list) to send multiple messages at once.\nEx.\n\n\033[94m  ctx\033[0m.\033[93mreply\033[0m([ msg1, msg2 ])\n\n")
        endpoint = api + "/message/reply"
        message = messages
        
        if not isinstance(message, list):
            message = [message]

        
        for i in range(len(message)):
            if (not isinstance(message[i], dict)) and (not isinstance(message[i], str)):
                message[i] = message[i].json
            elif isinstance(message[i], str):
                message[i] = {
                    "type": "text",
                    "text": message[i]
                }
        
        r = requests.post(endpoint, headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.CAT}"
        }, json={
            "replyToken": self.reply_token,
            "messages": message
        })
        #print(r.text)
        lineApiError(r.json())
        self.handled = True
        return r

    @property
    def get_user(self):
        """
        Fetch a user. Returns a `User` object.
    
        :param str CAT: Channel access token.
        :param str user_id: The user id.
        """
        CAT = self.CAT
        user_id = self.req['events'][0]['source']['userId']
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


class WebhookTextMessage(WM):
    def __init__(self, req: dict, CAT: str):
        e = req["events"][0]
        self.req = req # if needed

        self.CAT = CAT
       
        self.content = self.text = e["message"]["text"]
        self.message_id = self.id = e["message"]["id"]
        self.group = self.guild = self.server = None if (e['source']['type'] == "user") else e['source']['groupId']
        self.time = e['timestamp']
        self.reply_token = e['replyToken']

    @property
    def author(self):
        return super().get_user

    @property
    def user(self):
        return super().get_user

    def reply(self, messages: List[Union[TextMessage]]):
        super().reply(messages)

class WebhookStickerMessage(WM):
    def __init__(self, req: dict, CAT: str):
        e = req["events"][0]
        self.req = req

        self.CAT = CAT
        self.message_id = self.id = e["message"]['id']
        self.sticker_id = e["message"]["stickerId"]
        self.package_id = self.pack_id = e["message"]["packageId"]
        self.type = self.sticker_type = self.resource_type = e["message"]["stickerResourceType"].lower()
        try:
            self.sticker_keywords = self.keywords = e["message"]["keywords"]
        except:
            self.sticker_keywords = self.keywords = []
        self.group = self.guild = self.server = None if (e['source']['type'] == "user") else e['source']['groupId']
        self.time = e['timestamp']
        self.reply_token = e['replyToken']

    @property
    def author(self):
        return super().get_user

    @property
    def user(self):
        return super().get_user

    def reply(self, messages: List[Union[TextMessage]]):
        return super().reply(messages)

class WebhookVideoMessage(WM):
    def __init__(self, req: dict, CAT: str):
        e = req["events"][0]
        self.req = req # if needed
        self.CAT = CAT
        
        #self.author = self.user = super().get_user
        self.message_id = self.id = e["message"]["id"]
        #self.author = self.user = super().get_user
        self.group = self.guild = self.server = None if (e['source']['type'] == "user") else e['source']['groupId']
        self.time = e['timestamp']
        self.reply_token = e['replyToken']

        class Duration(object):
            def __init__(self, e: dict):
                self.dur = e["message"]["duration"]

            @property
            def ms(self):
                return self.dur

            @property
            def sec(self):
                return self.dur / 1000

            @property
            def full(self):
                return str(datetime.timedelta(seconds=round(self.dur / 1000)))
            
        self.duration = Duration(e)

    def reply(self, messages: List[Union[TextMessage]]):
        return super().reply(messages)

    @property
    def author(self):
        return super().get_user

    @property
    def user(self):
        return super().get_user

class WebhookLocationMessage(WM):
    def __init__(self, req: dict, CAT: str):
        e = req["events"][0]
        self.req = req # if needed
        self.CAT = CAT
        
        #self.author = self.user = super().get_user
        self.message_id = self.id = e["message"]["id"]
        #self.author = self.user = super().get_user
        self.group = self.guild = self.server = None if (e['source']['type'] == "user") else e['source']['groupId']
        self.time = e['timestamp']
        self.reply_token = e['replyToken']
        
        self.latitude = e["message"]["latitude"]
        self.longitude = e["message"]["longitude"]
        self.address = e["message"]["address"]

    def reply(self, messages: List[Union[TextMessage]]):
        return super().reply(messages)

    @property
    def author(self):
        return super().get_user

    @property
    def user(self):
        return super().get_user

class WebhookPostback(WM):
    def __init__(self, req: dict, CAT: str):
        e = req["events"][0]
        self.req = req # if needed
        self.CAT = CAT
        
        #self.author = self.user = super().get_user
        #self.author = self.user = super().get_user
        self.group = self.guild = self.server = None if (e['source']['type'] == "user") else e['source']['groupId']
        self.time = e['timestamp']
        self.reply_token = e['replyToken']
        
        self.data = self.content = e['postback']['data']

        if "params" in e["postback"]:
            self.datetime = e["postback"]["params"][list(e["postback"]["params"].keys())[0]]
        else:
            self.datetime = None

    def reply(self, messages: List[Union[TextMessage]]):
        super().reply(messages)

    @property
    def author(self):
        return super().get_user

    @property
    def user(self):
        return super().get_user
