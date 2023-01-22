from __future__ import annotations

import asyncio
import time
from termcolor import colored
from typing import Any

from .message import WBTextMessage, WBPostback
from ..connect.gate import reply as replyFunc
from ..exceptions import Usage as UsageError
from ..connect.fetch import profile

from .new import TextMessage
from ..tmp import Tmp

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
  
  def __init__(self, CAT: str, req: dict) -> BaseEvent:
    self.CAT = CAT
    self.req = req

    self.reply_token = req['replyToken']
    self.is_redelivery: bool = req['deliveryContext']['isRedelivery']
    self.event_id: str = req['webhookEventId']
    self.timestamp: int = req['timestamp']
    self.ping = ((time.time() * 1000) - req['timestamp'])
    self.replied = False
    self.t_queue = []


    async def init():
        self.author = self.user = await profile({
          "Authorization": "Bearer " + CAT
        }, req['source']['userId'])
        
    asyncio.run(init())

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
      TXT = "'text'"
      raise UsageError(
        "Usage Error", f"You could only use the reply function once. To send multiple messages, try this:\n\n{colored('await', 'magenta')} ctx.{colored('send', 'yellow')}([\n  message1,\n  message2\n])\n\nAlternatively, you can add options to the listener:\n\n{colored('@client.event', 'light_cyan')}({colored(TXT, 'yellow')}, {colored('linelib.utils.QueuedSending', 'light_green', attrs=['bold', 'blink'])})\n\nLinelib will then ignore this error."
      )

    for item in range(len(messages)):
      if isinstance(messages[item], str):
        messages[item] = TextMessage(messages[item]).json
        # in case we have to waste our time.

      if not isinstance(messages[item], dict):
        messages[item] = messages[item].json
        # the waffle house has found its new host

    if self.queued:
      if isinstance(messages, list):
        raise UsageError("QueuedSending", "In QueuedSending mode, you must not send multiple messages using a list. Instead, use the reply function twice.\nTo disable this, remove this option from the @decorator.")
      self.t_queue.append(messages)
    else:
      self.replied = True
      await self._startReply(messages, notification_disabled) # just reply it.

  async def _startReply(self, msg, notification_disabled: bool):
    """!important"""
    if not isinstance(msg, list):
      raise ValueError(
        "Must be list."
      )
    r = await replyFunc(self.client, self.reply_token, msg, notification_disabled)
    print(r.text)

  async def _exec(self):
    if self.queued and self.t_queue:
      await self._startReply(self.t_queue, False) # queued messages

  async def remember(self, key: Any, item: Any):
    Tmp.handle_action[self.TYPE][key] = item

  store = remember


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

    # ===========================

    self.send = self.reply # alias

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

    self.send = self.reply


# hello again!
# im really bored