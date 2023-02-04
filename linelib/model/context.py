from __future__ import annotations

import asyncio
import time
from termcolor import colored
from typing import Any, Literal

from .message import WBTextMessage, WBPostback, WBSticker

from ..connect.gate import reply as replyFunc
from ..connect.fetch import profile, profileAndGroup, getContent
from ..connect.types import Group, Profile

from ..exceptions import Usage as UsageError

from .new import TextMessage
from ..tmp import Tmp
from ..ext import Depends

class MessageObjects(list):
  """
  Message Objects based on a list.
  """

class BaseEvent:
  """
  Represents an event parent class.
  """
  # public:
  reply_token: str
  is_redelivery: bool
  event_id: str
  timestamp: int
  ping: float
  queued: bool = False
  author: Profile
  room_type: str
  
  def __init__(self, CAT: str, req: dict) -> BaseEvent:
    self.CAT = CAT
    self.req = req

    self.reply_token = req.get('replyToken', None)
    if not self.reply_token:
        self.reply = self.send = None
    self.is_redelivery: bool = req['deliveryContext']['isRedelivery']
    self.event_id: str = req['webhookEventId']
    self.timestamp: int = req['timestamp']
    self.ping = ((time.time() * 1000) - req['timestamp'])
    self.replied = False
    self.t_queue = []


    async def init():
        if req['source']['type'] == 'user':
            self.room_type = 'user'
            
            self.author = self.user = await profile({
                  "Authorization": "Bearer " + CAT
            }, req['source']['userId'])
            self.get_group = self.fetch_group = None
        else:
            self.room_type = 'group' # or multi-persons chat
            _profile, _groupCoroutineFunc = await profileAndGroup({
                "Authorization": "Bearer " + CAT
            }, req['source']['userId'], req['source']['groupId'])
            self.get_group = self.fetch_group = _groupCoroutineFunc
            self.author = self.user = _profile

    asyncio.run(init())

  async def get_group(self) -> Group | None:
      """
      (*New in version 2.2*)

      Fetches the current group. If this is a normal chatroom, this function does not exist.
      """
      pass # default

  async def reply(self, messages: MessageObjects = None, notification_disabled: bool = False, *args, **kwargs):
    """
    Replies the user.

    `messages` : MessageObjects

    The messages you want to send. `list` expected.

    ***

    `notification_disabled` : bool

    Whether to disable the push notifications for users. To disable, use `True`. Note that if the user has muted the chat / group, they will not receive any messages even though this is set to `False`.

    `*args, **kwargs` Arguments.
    """
    if not messages:
      messages = [
        TextMessage(*args, **kwargs)
      ]
    if not isinstance(messages, list):
      messages = [messages] # stupid way but why not

    if self.replied:
      raise UsageError(
        "Usage Error", f"You could only use the reply function once. To send multiple messages, try this:\n\n{colored('await', 'magenta')} ctx.{colored('send', 'yellow')}([\n  message1,\n  message2\n])\n\n"
      )

    for item in range(len(messages)):
      if isinstance(messages[item], str):
        messages[item] = TextMessage(messages[item]).json
        # in case we have to waste our time.

      if not isinstance(messages[item], dict):
        messages[item] = messages[item].json
        # the waffle house has found its new host

    await replyFunc(self.client, self.reply_token, messages, notification_disabled)

  async def remember(self, key: Any, item: Any):
    Tmp.handle_action[self.TYPE][key] = item

  store = remember
  send = reply


class TextMessageEvent(BaseEvent):
  """
  A LINE Text Message context.
  """
  message: WBTextMessage
  content: str
  text: str
  id: str
  client: type
  TYPE = 'text'

  def __init__(self, client, r):
    super().__init__(client.CAT, r)
    self.replied = False
    self.t_queue = []
    self.message = WBTextMessage(self.req)
    self.content = self.text = self.message.content # createAlias
    self.id = self.message.id
    self.client = client

class PostbackEvent(BaseEvent):
  """
  A LINE Postback Event.
  """
  data: str
  datetime: str | None
  rich_menu: str | None
  TYPE = 'postback'
  
  def __init__(self, client, r):
    super().__init__(client.CAT, r)
    self.client = client
    self.postback = WBPostback(r)
    self.data: str = self.postback.data
    self.datetime: str | None = self.postback.datetime
    self.rich_menu: str | None = self.postback.rich_menu

class StickerMessageEvent(BaseEvent):
    """
    A LINE Sticker Message Event.
    """
    sticker: WBSticker
    sticker_id: str
    package_id: str
    keywords: list[str]
    resource_type: Literal['static', 'animation', 'sound', 'animation_sound', 'popup', 'popup_sound', 'custom', 'message']
    TYPE = 'sticker'
    
    def __init__(self, client, r):
        super().__init__(client.CAT, r)
        self.client = client
        sticker = WBSticker(r)
        
        self.sticker_id = sticker
        self.package_id = sticker.package_id
        
        self.keywords = sticker.keywords
        self.resource_type = sticker.resource_type

        self.id = r['message']['id']

class UnsendEvent(BaseEvent):
    """
    Represents an unsend event.
    """
    message_id: str
    TYPE = 'unsend'
    
    def __init__(self, client, r):
        super().__init__(client.CAT, r)
        self.client = client
        self.message_id = self.id = r['unsend']['messageId']

class FollowEvent(BaseEvent):
    """
    Event object for when your LINE Official Account is added as a friend (or unblocked). You can reply to follow events.
    """
    TYPE = 'follow'
    
    def __init__(self, client, r):
        super().__init__(client.CAT, r)
        
        self.client = client
        
class UnfollowEvent(BaseEvent):
    """
    Event object for when your LINE Official Account is blocked.

    Note that **you cannot reply to this kind of event**.
    """
    TYPE = 'unfollow'
    
    def __init__(self, client, r):
        super().__init__(client.CAT, r)

        class Unavailable:
            def __str__(self):
                return '...'

            def __repr__(self):
                return '...'
        
        self.client = client

class JoinEvent(BaseEvent):
    """
    Event object for when your LINE Official Account joins a group chat or multi-person chat. You can reply to join events.

    - For group chats: A join event is sent when a user invites your LINE Official Account.

    - For multi-person chats: A join event is sent when the first event (for example when a user sends a message or is added to the multi-person chat) occurs after your LINE Official Account is added.
    """
    TYPE = "join"
    
    def __init__(self, client, r):
        super().__init__(client.CAT, r)

        self.client = client

class LeaveEvent(BaseEvent):
    """
    Event object for when a user removes your LINE Official Account from a group chat or when your LINE Official Account leaves a group chat or multi-person chat.
    """
    TYPE = "leave"
    
    def __init__(self, client, r):
        super().__init__(client.CAT, r)

        self.client = client

class MemberJoinEvent(BaseEvent):
    """
    Event object for when a user joins a group chat or multi-person chat that the LINE Official Account is in.
    """
    TYPE = "memberJoined"
    members: list

    def __init__(self, client, r):
        super().__init__(client.CAT, r)

        members = r['joined']['members']
        self.members = self.joined_members = [user['userId'] for user in members]

        self.client = client

class MemberLeaveEvent(BaseEvent):
    """
    Event object for when a user leaves a group chat or multi-person chat that the LINE Official Account is in.
    """
    TYPE = "memberLeft"

    def __init__(self, client, r):
        super().__init__(client.CAT, r)

        members = r['left']['members']
        self.members = self.left_members = [user['userId'] for user in members]

        self.client = client

class VideoViewingCompleteEvent(BaseEvent):
    """
    Event for when a user finishes viewing a video at least once with the specified `tracking_id` sent by the LINE Official Account.

    ## The number of video views
    A video viewing complete event doesn't necessarily indicate the number of times a user has watched a video.

    Watching a video multiple times in a single session in a chat room doesn't result in a duplicate event. However, if you close the chat room and reopen it to watch the video again, the event may reoccur.

    ## Video in imagemap messages and flex messages is not supported by the video viewing complete event
    The `tracking_id` can't be specified for a video in imagemap messages and flex messages.
    """
    TYPE = "videoPlayComplete"
    tracking_id: str

    def __init__(self, client, r):
        super().__init_(client.CAT, r)
        self.tracking_id = r['videoPlayComplete']['trackingId']

        self.client = client

class BeaconEvent(BaseEvent):
    """
    Event object for when a user enters the range of a [LINE Beacon](https://developers.line.biz/en/docs/messaging-api/using-beacons/). You can reply to beacon events.

    ## Possible Beacon Events
    - `enter` - Entered beacon's reception range.
    - `banner` - Tapped beacon banner. (Cooperated with LINE only)
    - `stay` - A user is within the range of the beacon's reception. This event is sent repeatedly at a minimum interval of 10 seconds.
    """
    TYPE = "beacon"
    hwid: str
    beacon_type: str
    dm: str | None

    def __init__(self, client, r):
        super().__init__(client.CAT, r)
        self.hwid = self.hardware_id = r['beacon']['hwid']
        self.type = self.beacon_type = r['beacon']['type']
        self.dm = self.device_message = r['beacon'].get('dm', None)
        self.client = client

class AccountLinkEvent(BaseEvent):
    """
    Event object for when a user has linked their LINE account with a provider's service account. You can reply to account link events.
    """
    TYPE = "accountLink"
    result: Literal['ok', 'failed']
    nonce: str
    
    def __init__(self, client, r):
        super().__init__(client.CAT, r)
        if not self.reply_token:
            # This property won't be included if linking the account has failed
            self.reply = self.send = None
        
        self.result: Literal['ok', 'failed'] = r['link']['result']
        self.nonce: str = r['link']['nonce']

        self.client = client

class SavableFile(BaseEvent):
    """
    This file could be downloaded and saved in your (local) environment.

    *New in v2.2*
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def save(self):
        """
        Save the document (file).
        """
        # fn: file name
        fn = await getContent(self.client.headers, self.id)
        return fn

class ImageMessageEvent(SavableFile):
    """
    Message object which contains the image content sent from the source.
    """
    TYPE = 'image'
    id: str
    content_provider: Literal['line', 'external']
    original_content_url: Depends[str]
    preview_image_url: Depends[str]
    image_sets: Depends[list]

    def __init__(self, client, r):
        super().__init__(client.CAT, r)
        req: dict = r['message']
        self.req = req
        self.client = client

        self.id = req['id']
        self.image_sets = req.get('imageSet', None)

        self.content_provider = self.provider = req['contentProvider']['type']
        
        if self.content_provider == 'external':
            self.original_content_url = req['contentProvider']['originalContentUrl']
            self.preview_image_url = req['contentProvider']['previewImageUrl']

class VideoMessageEvent(SavableFile):
    """
    Message object which contains the video content sent from the source. The preview image is displayed in the chat and the video is played when the image is tapped.
    """
    TYPE = 'video'
    id: str
    content_provider: Literal['line', 'external']
    original_content_url: Depends[str]
    preview_image_url: Depends[str]
    duration: int # mileseconds

    def __init__(self, client, r):
        super().__init__(client.CAT, r)
        req: dict = r['message']
        self.req = req
        self.client = client

        self.id = req['id']
        self.duration = req.get('duration', None)
        self.content_provider = self.provider = req['contentProvider']['type']
        
        if self.content_provider == 'external':
            self.original_content_url = req['contentProvider']['originalContentUrl']
            self.preview_image_url = req['contentProvider']['previewImageUrl']

class AudioMessageEvent(SavableFile):
    """
    Message object which contains the audio content sent from the source.
    """
    TYPE = 'audio'
    id: str
    content_provider: Literal['line', 'external']
    original_content_url: Depends[str]
    preview_image_url: str
    duration: int # mileseconds

    def __init__(self, client, r):
        super().__init__(client.CAT, r)
        req: dict = r['message']
        self.req = req
        self.client = client

        self.id = req['id']
        self.duration = req.get('duration', None)
        self.content_provider = self.provider = req['contentProvider']['type']
        if self.provider == 'external':
            self.original_content_url = req['contentProvider']['originalContentUrl']



class FileMessageEvent(SavableFile):
    """
    Message object which contains the file sent from the source. The binary data of the file can be retrieved by specifying the message ID and calling the API.
    """
    TYPE = 'file'
    file_name: str
    file_size: int # in bytes
    
    def __init__(self, client, r):
        super().__init__(client.CAT, r)
        req: dict = r['message']
        self.req = req

        self.id = req['id']
        self.file_name = self.name = req['fileName']
        self.file_size = self.size = req['fileSize']

        self.client = client

class LocationMessageEvent(BaseEvent):
    """
    Message object which contains the location data sent from the source.
    """
    TYPE = 'location'
    id: str
    title: Depends[str]
    address: Depends[str]

    latitude: float
    longitude: float

    def __init__(self, client, r):
        super().__init__(client.CAT, r)
        self.req = req = r['message']
        self.id = req['id']
        
        self.title = req.get('title', None)
        self.address = req.get('address', None)
        
        self.latitude = req['latitude']
        self.longitude = req['longitude']

        self.client = client



# hello again!
# im really bored