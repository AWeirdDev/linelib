from __future__ import annotations

import re
import uuid
from typing import (List, Literal, Any)
from inspect import iscoroutinefunction as isCoro
from termcolor import colored

from ..exceptions import Async
from ..tmp import Tmp
from ..ext import Depends

# consts
PREFIX = colored('linelib v2', 'light_green')

class ms(int):
  pass

class Decimal(float):
  pass

class TextMessage:
  """
  Represents a text message.

  `text` : str

  The message text (PLAIN TEXT). (e.g., `help me!`)

  ***

  `emojis` : List[Emoji | dict]

  The LINE emojis that are going to be 'injected' into your text.

  To do so, **you will need to make sure to add '$' into your text, just to make us easier to see where we should put a specified emoji.**

  Or, you can use this format: `<product id:emoji id>`. (Designed for lazy people like me)

  **Cool Example 1**

  ```py
  TextMessage(
    "help me... $ I'm stuck in this documentation... $",
    emojis=[
      Emoji('product id', 'emoji id'), # first '$'
      Emoji('product id', 'emoji id') # second '$'
    ]
  )
  ```

  **Epic Example 2**

  ```py
  # mode: lazy
  TextMessage(
    "I am happy. <product id:emoji id> What about you? <product id:emoji id>"
  )
  ```

  > Note: If you really want to disable this kind of mode, try this:

  ```py
  TextMessage(
    "disabled-lazy:Message content here! <wont:work!>"
  )
  ```

  ***

  `quick_reply` : dict | QuickReply

  Quick reply buttons. They will display on the bottom of the screen. 

  ***

  `sender` : dict | Sender

  Send messages with specified profile pictures and names. Note that the name of it will display like this (assuming the original bot name is **Cool Guy**, and the sender name is **Bad Guy**: `'Bad Guy' from Cool Guy` (that's odd)

  """

  def __init__(self,
               text: str,
               emojis: List[Emoji | dict] = None,
               quick_reply: QuickReply = None,
               sender: dict | Sender = None):
    pattern: str = '\<.*\:.*>'
    if re.findall(pattern, text):
      if text.startswith('disabled-lazy:'):
        text = text.replace('disabled-lazy:', '', 1)
      else:
        emojis = []
        for result in re.findall(pattern, text):
          formatted_result = result.replace("<", "").replace(">",
                                                             "").split(":")
          productId = formatted_result[0]  # < Here! : ... >
          emojiId = formatted_result[1]  # < ... : Here! >
          text = text.replace(result, "$")  # cool!
          emojis.append(Emoji(productId, emojiId))
          # ...and then the next part will parse it!

    if emojis:
      parsed_emojis = []
      cur = 0
      for i in re.finditer("\$", text):
        index = i.start()
        json = emojis[cur].json
        json['index'] = index
        parsed_emojis.append(json)
        cur += 1
      # overwrite be like:
      emojis = parsed_emojis  # noqa

    self.json = {
      "type": "text",
      "text": text,
      "emojis": emojis,
      "quickReply": getattr(quick_reply, "json", None) or quick_reply,
      # getattr(sender, "json", None):
      # finds the attribute of "json" of the sender (object?) argument
      # if the attribute was not found, returns None
      # ---------------
      # ... or sender:
      # if the previous statement returns 'None'
      # returns the original sender (JSON)
      "sender": getattr(sender, "json", None) or sender
    }


class Emoji:
  """
  Represents a LINE emoji. You can add it to your `TextMessage` constructors!

  See [List of Available Emojis](https://developers.line.biz/en/docs/messaging-api/emoji-list/)

  `product_id` : str

  The Product ID.

  ***

  `emoji_id` : str

  The Emoji ID.
  
  """

  def __init__(self, product_id: str, emoji_id: str):
    self.json = {
      "productId": product_id,
      "emojiId": emoji_id,
      "index": 'undefined'
    }

  @property
  def product_id(self):
    return self.json['productId']

  @property
  def emoji_id(self):
    return self.json['emojiId']

  @property
  def index(self):
    return self.json['index']


class Sender:
  """
  When sending a message from the LINE Official Account, you can specify the name and the icon_url arguments.

  `name` : str

  Display name.

  ***
  
  `icon_url` : str

  URL of the image to display as an icon when sending a message.
  """

  def __init__(self, name: str = None, icon_url: str = None):
    self.json = {"name": name, "iconUrl": icon_url}


class QuickReply:
  """
  Quicky Quick Reply.

  `items` : List[QuickReplyButton, dict]

  The button objects to display within a row.
  """

  def __init__(self, items: List[QuickReplyButton, dict]):
    done = []
    for i in items:
      done.append(getattr(i, "json", None) or i)
    self.json = {"items": done}


class QuickReplyButton:
  """
  A QuickReply button.

  `action` : PostbackAction | MessageAction | URIAction | DatetimePickerAction | CameraAction | CameraRollAction | LocationAction | RichMenuSwitchAction | dict

  Action performed when this button is tapped. The following is available:

  - Postback
  - Message
  - URI
  - Datetime
  - Camera
  - Camera Roll
  - Location
  - Rich Menu Switch

  `image_url` : str

  URL of the icon at the beginning of the button.
  """

  def __init__(self,
               action: PostbackAction | MessageAction | URIAction
               | DatetimePickerAction | CameraAction | CameraRollAction
               | LocationAction | RichMenuSwitchAction | dict,
               image_url: str = None):
    self.json = {
      "type": "action",
      "action": getattr(action, "json", None) or action,
      "imageUrl": image_url
    }


class HandlableAction:
  def __init__(self, aType):
    self.json = {}
    self.aType = aType
    self.STORE = {}  # : Empty

  async def remember(self, key: Any, item: Any) -> None:
    Tmp.action_storage[self.DATA] = {}
    Tmp.action_storage[self.DATA][key] = item
  
  store = remember

  def handle(self):
    """
    Handles the action.
    """

    def wrapper(func, *args, **kwargs):
      if not isCoro(func):
        raise Async(
          'Async Function',
          f"Function '{func.__name__}' should be an async function.")

      Tmp.self_handler[self.DATA] = func

      return func

    return wrapper

  def store(self, *key, **items):
    """
    Stores further information for this action object. You could get them from whether `@client.event(...)`, or `@ACTION.handle()`! Use `ctx.stored` to fetch them!

    **Example:** `store(epic='yes', super='cool')`

    **Get:** `ctx.stored.super` (returns `"cool"`)
    """
    self.STORE = items  # dict


class PostbackAction(HandlableAction):
  """
  When a control associated with this action is tapped, a postback event is returned via webhook with the specified string in the `data` property.

  `data` : str

  A developer-defined custom ID. You could leave this blank.
  
  `label` : str

  The text displays on the button.

  
  `display_text` : str

  The text that will be sent once the user clicked on the button.

  `input_option`: Literal['close_rich_menu', 'open_rich_menu', 'open_keyboard', 'open_voice']

  The display method of such as rich menu based on user action. Specify one of the following values:

  `close_rich_menu`: Close rich menu
  `open_rich_menu`: Open rich menu
  `open_keyboard`: Open keyboard
  `open_voice`: Open voice message input mode
  
  This is available on LINE version `12.6.0` or later for iOS or Android.

  
  `fill_in_text` : str

  String to be pre-filled in the input field when the keyboard is opened. Valid only when the `input_option` argument is set to `open_keyboard`. The string can be broken by a newline character (`\n`).
  """

  def __init__(self,
               data: str = None,
               label: str = None,
               display_text: str = None,
               input_option: Literal['close_rich_menu', 'open_rich_menu',
                                     'open_keyboard', 'open_voice'] = None,
               fill_in_text: str = None):
    super().__init__('postback')
    if (input_option != "open_keyboard") and fill_in_text:
      raise ValueError(
        "\n\n`input_option` must be 'open_keyboard' in order to make your `fill_in_text` to work."
      )
    self.DATA = data or str(uuid.uuid4())
    self.json = {
      "type": 'postback',
      "data": self.DATA,
      "label": label,
      "displayText": display_text,
      "inputOption": {
        "close_rich_menu": "closeRichMenu",
        "open_rich_menu": "openRichMenu",
        "open_keyboard": "openKeyboard",
        "open_voice": "openVoice"
      }.get(input_option),
      "fillInText": fill_in_text
    }


class MessageAction:
  """
  When a control associated with this action is tapped, the specified text is sent as a message from the user.

  `text` : str

  The text that'll be sent once the button got clicked.

  ***

  `label` : str ~ **Depends**

  Label for the action. The specification depends on which object the action is set to.
  """

  def __init__(self, text: str, label: Depends[str] = None):
    self.json = {"type": "message", "label": label, "text": text}


class URIAction:
  """
  When a control associated with this action is tapped, the URI specified in the uri argument is opened in LINE's in-app browser.

  `uri` : str

  URI opened when the action is performed (Max character limit: 1000). The available schemes are `http`, `https`, `line` *(deprecated)*, and `tel`. **`tel` example: `tel:09001234567`**

  ***

  `label` : str ~ **Depends**

  Label for the action. The specification depends on which object the action is set to.

  ***
  
  `alt_uri_desktop` : str ~ **Depends**

  **IMPORTANT: This is only supported when you set URI actions in Flex Messages, but it doesn't work in quick reply.**
  
  URI opened on LINE for **macOS** and **Windows** when the action is performed (Max character limit: 1000). If the `alt_uri_desktop` argument is set, the `uri` argument is ignored on LINE for macOS and Windows. The available schemes are `http`, `https`, `line` *(deprecated)*, and `tel`. **`tel` example: `tel:09001234567`**
  """

  def __init__(self,
               uri: str,
               label: Depends[str] = None,
               alt_uri_desktop: Depends[str] = None):
    self.json = {
      "type": "uri",
      "label": label,
      "uri": uri,
      "altUri": {
        "desktop": alt_uri_desktop
      }
    }


class DatetimePickerAction(HandlableAction):
  """
  When a control associated with this action is tapped, a postback event is returned via webhook with the date and time selected by the user from the date and time selection dialog. The datetime picker action does not support time zones.

  ***

  ### Date and time format
  The date and time formats for the initial, max, and min values are shown below. The full-date, time-hour, and time-minute formats follow the [RFC3339](https://www.ietf.org/rfc/rfc3339.txt) protocol.

  <table>
    <thead>
      <tr>
        <th>Mode</th>
        <th>Format</th>
        <th>Example</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>date</td>
        <td><code>full-date</code><br />Max: 2100-12-31<br />Min: 1900-01-01</td>
        <td>2017-06-18</td>
      </tr>
      <tr>
        <td>time</td>
        <td><code>time-hour:time-minute</code><br />Max: 23:59<br />Min: 00:00</td>
        <td>12:50</td>
      </tr>
      <tr>
        <td>datetime</td>
        <td><code>full-dateTtime-hour:time-minute or full-datettime-hour:time-minute</code><br />Max: 2100-12-31T23:59<br />Min: 1900-01-01T00:00</td>
        <td>2017-06-18T06:15</td>
      </tr>
    </tbody>
  </table>

  ***

  ### Parameters

  `mode` : Literal['date', 'time', 'datetime']

  Action (picker) mode

  - `date`: Pick date
  - `time`: Pick time
  - `datetime`: Pick date and time

  ***

  `data` : str

  Developer-defined custom ID. You can leave this blank.

  ***

  `label` : str ~ **Depends**

  Label for the action. The specification depends on which object the action is set to.

  ***

  `initial` : str

  Initial (aka. default) value of date or time.

  ***

  `max` : str

  Largest date or time value that can be selected. Must be greater than the `min` value.

  ***

  `min` : str

  Smallest date or time value that can be selected. Must be less than the `max` value.
  """

  def __init__(self,
               mode: Literal['date', 'time', 'datetime'],
               data: str = None,
               label: Depends[str] = None,
               initial: str = None,
               max: str = None,
               min: str = None):
    self.DATA = data or str(uuid.uuid4())
    self.json = {
      "type": "datetimepicker",
      "label": label,
      "data": self.DATA,
      "mode": mode,
      "initial": initial,
      "max": max,
      "min": min
    }


class CameraAction:
  """
  **This action can be configured only with quick reply buttons.** When a button associated with this action is tapped, the camera screen in LINE is opened.
  """

  def __init__(self, label: str):
    self.json = {"type": "camera", "label": label}


class CameraRollAction:
  """
  **This action can be configured only with quick reply buttons.** When a button associated with this action is tapped, the camera roll screen (also known as image selector) in LINE is opened.
  """

  def __init__(self, label: str):
    self.json = {"type": "cameraRoll", "label": label}


class LocationAction:
  """
  **This action can be configured only with quick reply buttons.** When a button associated with this action is tapped, the location screen in LINE is opened.
  """

  def __init__(self, label: str):
    self.json = {'type': 'location', 'label': label}


class RichMenuSwitchAction(HandlableAction):
  """
  **This action can be configured only with rich menus.**

  When you tap a rich menu associated with this action, you can switch between rich menus, and a postback event including the rich menu alias ID selected by the user is returned via a webhook.

  `rich_menu_alias_id` : str

  Rich menu alias ID to switch to.

  ***
  
  `data` : str

  A developer-defined custom ID. You could leave this blank.

  ***
  
  `label` : str ~ Optional

  Action label. Optional for rich menus. Read when the user's device **accessibility feature** is enabled.
  
  """

  def __init__(self, rich_menu_alias_id, data: str = None, label: str = None):
    self.DATA = data or str(uuid.uuid4())
    self.json = {
      "richMenuAliasId": rich_menu_alias_id,
      "data": self.DATA,
      "label": label
    }

class StickerMessage:
  """
  Represents a sticker-only message.

  See [List of Available Stickers ↗](https://developers.line.biz/en/docs/messaging-api/sticker-list/)

  ***

  `package_id` : str

  Package ID for a set of stickers. For information on package IDs, see the List of available stickers.

  `sticker_id` : str

  Sticker ID. For a list of sticker IDs for stickers that can be sent with the Messaging API, see the List of available stickers.
  """
  def __init__(self, package_id: str, sticker_id: str):
    self.json = {
      "type": "sticker",
      "packageId": package_id,
      "stickerId": sticker_id
    }

class ImageMessage:
  """
  Represents an image message.

  Each URL must follow:
  
  - `http` OR `https`
  - `JPEG` or `PNG`
  
  ***

  `original` : str

  The original content URL. (Max file size: `10MB`)

  ***
  
  `preview` : str

  The preview image URL (zipped, for thumbnails). (Max file size: `1MB`)
  """
  def __init__(self, original: str, preview: str):
    self.json = {
      "type": "image",
      "originalContentUrl": original,
      "previewImageUrl": preview
    }

class VideoMessage:
  """
  Represents a video message.

  ***
  
  ### Video Aspect Ratio
  - A very wide or tall video may be cropped when played in some environments.
  - The aspect ratio of the video specified in `original` and the preview image specified in `preview_image` should be the same. If the aspect ratio is different, a preview image will appear behind the video.
  
  ***

  `original` : str

  URL of video file (Max character limit: 2000)
  
  - HTTPS over TLS 1.2 or later
  - mp4
  - Max file size: 200 MB

  ***

  `preview_image` : str

  URL of preview image (Max character limit: 2000)
  
  - HTTPS over TLS 1.2 or later
  - JPEG or PNG
  - Max file size: 1 MB

  ***

  `tracking_id` : str

  ID used to identify the video when Video viewing complete event occurs. If you send a video message with `tracking_id` added, the video viewing complete event occurs when the user finishes watching the video.

  You can use the same ID in multiple messages.

  """
  def __init__(self, original: str, preview_image: str, tracking_id: str = None):
    self.json = {
      "type": "video",
      "originalContentUrl": original,
      "previewImageUrl": preview_image,
      "trackingId": tracking_id
    }

class AudioMessage:
  """
  Represents an audio message.

  ***

  `original` : str

  URL of audio file (Max character limit: 2000)

  - HTTPS over TLS 1.2 or later
  - m4a
  - Max file size: 200 MB

  **Notice**
  ```
  Only M4A files are supported on the Messaging API. If a service only supports MP3 files, you can use a service like FFmpeg to convert the files to M4A.
  ```

  ***

  `duration` : ms

  Length of audio file (milliseconds)
  """
  def __init__(self, original: str, duration: ms):
    self.json = {
      "type": 'audio',
      'originalContentUrl': original,
      'duration': duration
    }

class LocationMessage:
  """
  Represents a location message.

  ***

  `title` : str

  Title, Max character limit: 100. (e.g. `My Location`)

  ***
  
  `address` : str

  Address, Max character limit: 100. (e.g., `1-6-1 Yotsuya, Shinjuku-ku, Tokyo, 160-0004, Japan`)

  ***

  `latitude` : Decimal

  Latitude. (e.g., `35.687574`)

  ***
  
  `longitude` : Decimal

  Longitude. (e.g., `139.72922`)
  
  """
  def __init__(self, title: str, address: str, latitude: Decimal, longitude: Decimal):
    self.json = {
      'type': 'location',
      'title': title,
      'address': address,
      'latitude': latitude,
      'longitude': longitude
    }

class ImagemapMessage:
  """
  [See Documentation (please) ↗](https://developers.line.biz/en/reference/messaging-api/#imagemap-message)
  
  Imagemap messages are messages configured with an image that has multiple tappable areas. You can assign one tappable area for the entire image or different tappable areas on divided areas of the image.

  You can also play a video on the image and display a label with a hyperlink after the video is finished.
  """
  def __init__(self, base_url: str, alt_text: str, base_size: BaseSize | dict, video: Video | dict, actions: List[IMURIAction, IMMessageAction]):
    self.json = { # i hate this >:(
      "baseUrl": base_url,
      "altText": alt_text,
      "baseSize": base_size,
      "video": video,
      "actions": actions
    }


def BaseSize(width: int, height: int):
  return {
    "width": int,
    "height": height
  }


def Video(original: str, preview: str, area: ImagemapArea | dict, external_link: ExternalLink | dict):
  return {
    "originalContentUrl": original,
    "previewImageUrl": preview,
    "area": area,
    "externalLink": external_link
  }

def ImagemapArea(x: int, y: int, width: int, height: int):
  return {
    "x": x,
    "y": y,
    "width": width,
    "height": height
  }

def ExternalLink(link: str, label: str):
  return {
    "linkUri": link,
    "label": label
  }

def IMURIAction(uri: str, area: ImagemapArea | dict, label: str = None):
  return {
    "type": "uri",
    "label": label,
    "linkUri": uri,
    "area": area
  }

def IMMessageAction(text: str, area: ImagemapArea | dict, label: str = None):
  return {
    "type": "message",
    "label": label,
    "text": text,
    "area": area
  }

