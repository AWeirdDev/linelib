from __future__ import annotations

import aiohttp

from ..construct import utils

def _api(url):
  return "https://notify-api.line.me/api/" + url.replace('.', '/')

class Notify:
  """
  [LINE Notify.](https://notify-bot.line.me)
  """
  def __init__(self, access_token: str):
    self.AT: str = access_token
    self.headers: dict = {
      "Authorization": "Bearer " + access_token,
      "Content-Type": "application/x-www-form-urlencoded"
    }

  async def notify(self, message: str, image_thumbnail: utils.URL = "", image_full_size: utils.URL = "", notification_disabled: bool = False):
    """
    Send a notification through LINE Notify.

    message : str

    The message content. (MAX: 1000 characters)

    image_thumbnail, image_full_size : URL

    Should be both set at the same time.

    - `image_thumbnail`: 240×240px JPEG
    - `image_full_size`: 2048×2048px JPEG

    notification_disabled : bool

    When set to `True`, the user will not receive a push message. However, even though it's set to `False` -- which means normally you will receive a push message -- if some users muted the group / bot, this will not work.
    """
    if image_thumbnail:
      image_full_size = image_thumbnail
    elif image_full_size:
      image_thumbnail = image_full_size


    async with aiohttp.ClientSession() as session:
      async with session.post(_api('notify'), headers=self.headers, params={
        "message": message,
        "imageThumbnail": image_thumbnail,
        "imageFullsize": image_full_size,
        "notification_disabled": {True: "true", False: "false"}[notification_disabled]
      }) as resp:
        return resp

  async def status(self):
    async with aiohttp.ClientSession() as session:
      async with session.get(_api('status'), headers=self.headers) as resp:
        json = await resp.json()
        
        class Response:
          status: int = resp.status
          message: str = json['message']
          target_type: str = json['targetType']
          target: str = json['target']

        return Response