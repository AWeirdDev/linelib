"""
Linelib Utils.
"""

from __future__ import annotations

from .model.context import TextMessageEvent, PostbackEvent, StickerMessageEvent, UnsendEvent, FollowEvent, UnfollowEvent, MemberJoinEvent, MemberLeaveEvent, VideoViewingCompleteEvent, BeaconEvent, AccountLinkEvent, ImageMessageEvent, VideoMessageEvent, AudioMessageEvent, FileMessageEvent, LocationMessageEvent, JoinEvent, LeaveEvent

from .tmp import Tmp
from .exceptions import Invalid


class EventObject(object):
  """
  An event object returned from `@client.event`
  """

  def __init__(self, to: dict):
    self.func = to['func']
    self.type = to['type']
    self.options = to['options']  # additional context / options

  async def emit(self, *args, **kwargs):
    await self.func(*args, **kwargs)


def modifiable(*_, **params):
  """
  Represents a function (Any) is modifiable — which means in the subclass, it could be overwritten.
  """

  def wrapper(func):
    return func

  return wrapper


def getTriggerType(req: dict):
  if req['type'] == 'message':
    return req['message']['type']
  else:
    return req['type']


def getContext(_type: str, client, req) -> type:
  context = ({
      "text": TextMessageEvent,
      "postback": PostbackEvent,
      "sticker": StickerMessageEvent,
      "unsend": UnsendEvent,
      "follow": FollowEvent,
      "unfollow": UnfollowEvent,
      "join": JoinEvent,
      "leave": LeaveEvent,
      "memberJoined": MemberJoinEvent,
      "memberLeft": MemberLeaveEvent,
      "videoPlayComplete": VideoViewingCompleteEvent,
      "beacon": BeaconEvent,
      "accountLink": AccountLinkEvent,
      "image": ImageMessageEvent,
      "video": VideoMessageEvent,
      "audio": AudioMessageEvent,
      "file": FileMessageEvent,
      "location": LocationMessageEvent,
  }[_type](
    client,  # Client
    req  # request dictionary (aka. json)
  ))
  context.stored = context.memory = Tmp.handle_action[_type]
  if _type == 'postback':
    context.action_stored = Tmp.action_storage[context.data]

  return context


class utils:
  """
  Linelib utils.
  """

  class _noInit:

    def __init__(self, *args, **kwargs):
      raise Invalid(
        "No Construct",
        "Please do not construct this class. In other words, DO NOT add `(...)` on the right of the class."
      )
    
  class _str:
    def __matmul__(self, other):
      return other
  
  String = _str()

  class QueuedSending(_noInit):
    """
    # Deprecated.
    """
    ACTIVE = True

  class URL(str):
    def __repr__(self):
      return "<linelib URL>"

  class MessageObjects(list):
    """
    Linelib message objects. Should be a list of message classes. (constructed)
    """
    pass


class _method:
  method = "@NotMentioned"

  def __getitem__(self, key):
    self.method = key

  def __repr__(self):
    return f"<Method method='{self.method}'>"


Method = _method()
