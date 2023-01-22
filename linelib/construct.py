"""
Linelib Utils.
"""

from __future__ import annotations

from .model.context import (TextMessageEvent, PostbackEvent)

from .tmp import Tmp
from .exceptions import Invalid


class EventObject(object):
  """
  An event object returned from `@client.event`
  """

  def __init__(self, to: dict):
    self.func = to['func']
    self.type = to['type']
    #print(to['options'])
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
    "postback": PostbackEvent
  }[_type](
    client,  # Client
    req  # request dictionary (aka. json)
  ))
  context.stored = Tmp.handle_action[_type]
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

  class QueuedSending(_noInit):
    """
    Queued message sending.

    Due to line API limits, we can only send **one request for each reply**, but it's possible to contain multiple messages per request.

    Usually, linelib will raise an error when you use the `reply` method twice, or more.

    But with `QueuedSending`, it is possible to use the `reply` method for multiple times, but the message will be queued.

    This is the perfect tool when you're not quite used to using the listed-sending method. (aka. discord library users)

    **Example with `QueuedSending`**
    ```py
    await ctx.reply('some message')
    time.sleep(1) # some task
    await ctx.reply('boo!')
    ```
    ⬇️ BECOMES ⬇️
    ```py
    time.sleep(1) # some task
    await ctx.reply([
      'some message',
      'boo!'
    ])
    ```
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
