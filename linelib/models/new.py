import re
import uuid
from typing import Union, List, Literal

from ..logger import Logger
from ..database import db
from ..errors import lineApiError
from .types import ms


class Emoji(object):
    """
Represents a LINE emoji.

:param str product_id: The emoji product ID. Example: `5ac1bfd5040ab15980c9b435`
:param str emoji_id: The emoji ID within the product (emoji pack). Example: `001`, `002`...
    """

    def __init__(self, product_id: str, emoji_id: str):
        self.product_id = product_id
        self.emoji_id = emoji_id
        self.json = {
            "productId": product_id,
            "emojiId": emoji_id,
            "index": "undefined"  # not defined
        }

class StickerMessage:
    """
    LINE Sticker.

    ## Parameters
    package_id : str
    
        Package ID for a set of stickers. For information on package IDs, see the [List of available stickers](https://developers.line.biz/en/docs/messaging-api/sticker-list/).

    sticker_id : str
    
        Sticker ID. For a list of sticker IDs for stickers that can be sent with the Messaging API, see the [List of available stickers](https://developers.line.biz/en/docs/messaging-api/sticker-list/).
    """
    def __init__(self, package_id: str, sticker_id: str):
        self.package_id = package_id
        self.sticker_id = sticker_id
        self.json = {
            "type": "sticker",
            "packageId": package_id,
            "stickerId": sticker_id,
            "index": "undefined"  # not defined
        }

class ImageMessage:
    """
    Image message.

    ## Parameters
    original_content_url : str

        Image URL, JPEG or PNG.

    preview_image_url : str = None

        Preview Image URL, JPEG or PNG.
    """
    def __init__(self, original_content_url: str, preview_image_url: str = None):
        self.json = {
            "type": "image",
            "originalContentUrl": original_content_url,
            "previewImageUrl": preview_image_url or original_content_url
        }


class Action(object):
    """
Represents an action. It clearly does nothing.

Resources
---------
[LINE API Docs](https://developers.line.biz/en/reference/messaging-api/#action-objects)
    """
    pass
    


class PostbackAction(Action):
    r"""
Represents a Postback Action.

Parameters
----------

label : str = None

    The label, the specification depends on which object the action is set to. Please also see the [description](https://developers.line.biz/en/reference/messaging-api/#postback-action).

display_text : str = None

    Text displayed in the chat as a message sent by the user when the action is performed. Required for quick reply buttons, optional for other message types.

data : str = None

    String returned via webhook in the `postback.data` property. It's a kind of `custom_id`.
    If you're using `LINELIB`'s PostBack handler, you don't need to set this since the requested value is stored in a temporary database.


input_option : str = None

    The display method of such as rich menu based on user action. Could be one of `closeRichMenu`, `openRichMenu`, `openKeyboard`, or `openVoice`.

fill_in_text : str = None

    String to be pre-filled in the input field when the keyboard is opened. Valid only when the `input_option` argument is set to `openKeyboard`. The string can be broken by a newline character (`\n`).
    """

    def __init__(self,
                 label: str = None,
                 data: str = None,
                 display_text: str = None,
                 input_option: Literal["closeRichMenu", "openRichMenu",
                                       "openKeyboard", "openVoice"] = None,
                 fill_in_text: str = None, *handlerArgs, **handlerKwargs):
        self.process_id = str(uuid.uuid4())
        
        
        if not data:
            self.ref = handlerKwargs
            db.handlers[self.process_id] = self._trigger
            data = self.process_id

        self.json = {
            "type": "postback",  # REQUIRED
            "label": label,
            "data": data,
            "displayText": display_text,
            "inputOption": input_option,
            "fillInText": fill_in_text
        }
        self.handler = None

    def _trigger(self, res):
        if self.handler:
            self.handler(ctx=res, **self.ref)

    def handle(self):
        """
        Handles the event.
        """
        def wrapper(f, *args, **kwargs):
            self.handler = f
            return f
        return wrapper


class DateTimePickerAction(Action):
    """
    When a control associated with this action is tapped, a `postback` event is returned via webhook with the date and time selected by the user from the date and time selection dialog. The datetime picker action does not support time zones.

    Parameters
    ----------

    mode : Literal["date", "time", "datetime"]
        Action mode
        `date`: Pick date — Ex. `2022-10-10`
        `time`: Pick time — Ex. `17:00`
        `datetime`: Pick date and time — Ex. `2022-10-10t17:00`

    data : str = None
        String returned via webhook in the `postback.data` property. It's a kind of `custom_id`.
        If you're using `LINELIB`'s PostBack handler, you don't need to set this since the requested value is stored in a temporary database.


    label : str = None
        Label for the action. The specification depends on which object the action is set to. See [description](https://developers.line.biz/en/reference/messaging-api/#datetime-picker-action).

    initial : str = None
        Initial (aka. default) value of date or time.
        For the format, see description for argument `mode`.

    max : str = None
        Largest date or time value that can be selected. Must be greater than the `min` value.
        For the format, see description for argument `mode`.

    min : str = None
        Smallest date or time value that can be selected. Must be less than the `max` value.
        For the format, see description for argument `mode`.
    """
    def __init__(self, mode: Literal["date", "datetime", "time"], data: str=None, label: str=None, initial: str=None, max: str=None, min: str=None, *handlerArgs, **handlerKwargs):
        self.process_id = str(uuid.uuid4())
        
        
        if not data:
            self.ref = handlerKwargs
            db.handlers[self.process_id] = self._trigger
            data = self.process_id

        self.handler = None
        self.json = {
            "type": "datetimepicker",
            "data": data,
            "mode": mode,
            "label": label,
            "initial": initial,
            "max": max,
            "min": min
        }

    def _trigger(self, res):
        if self.handler:
            self.handler(ctx=res, **self.ref)

    def handle(self):
        """
        Handles the event.
        """
        def wrapper(f, *args, **kwargs):
            self.handler = f
            return f
        return wrapper
        

class URIAction(Action):
    """
    When a control associated with this action is tapped, the URI specified in the `uri` property is opened in LINE's in-app browser.

    Parameters
    ----------

    uri : str
        URI opened when the action is performed.
        The available schemes are http, https, line, and tel.
        (Max character limit: 1000)

    label : str
        Label for the action. The specification depends on which object the action is set to. See [description](https://developers.line.biz/en/reference/messaging-api/#uri-action).

    alt_uri_desktop : str
        URI opened on LINE for macOS and Windows when the action is performed.
        The available schemes are http, https, line, and tel.
        (Max character limit: 1000)
        > Note: The alt_uri_desktop is supported when you set URI actions in Flex Messages, but it doesn't work in quick reply.
    """

    def __init__(self,
                 uri: str,
                 label: str = None,
                 alt_uri_desktop: str = None):
        self.json = {
            "type": "uri",
            "label": label,
            "uri": uri,
            "altUri": {
                "desktop": alt_uri_desktop
            }
        }


class CameraAction(Action):
    """
    This action can be configured only with quick reply buttons. When a button associated with this action is tapped, the camera screen in LINE is opened.
    
    :param str label: Label.
    """
    def __init__(self, label: str):
        self.json = {
            "type": "camera",
            "label": label
        }

class CameraRollAction(Action):
    """
    This action can be configured only with quick reply buttons. When a button associated with this action is tapped, the camera roll screen in LINE is opened.

    :param str label: Label.
    """
    def __init__(self, label: str):
        self.json = {
            "type": "cameraRoll",
            "label": label
        }

class MessageAction(Action):
    """
    Represents a Message Action.

    Parameters
    ----------

    text : str
        The text to be sent by the user.

    label : str = None
        The display label.
        See [description](https://developers.line.biz/en/reference/messaging-api/#message-action) for the `label` parameter.
    
    """

    def __init__(self, text: str, label: str = None):
        self.json = {"type": "message", "text": text, "label": label}


class QuickReplyButton(object):
    """
Buttons for `QuickReply`.

Resources
---------
[LINE API Docs](https://developers.line.biz/en/reference/messaging-api/#quick-reply)

Parameters
----------
`action` : Union[PostbackAction, MessageAction, URIAction]
Action.

`image_url`: str=None
URL of the icon that is displayed at the beginning of the button
- Max character limit: 2000
- URL scheme: https
- Image format: PNG
- Aspect ratio: 1:1
- Data size: Up to 1 MB

1. There is no limit on the image size.
2. If the action property has a camera action, camera roll action, or location action, and the `imageUrl` property is not set, the *default icon* is displayed.
    """

    def __init__(self,
                 action: Union[PostbackAction, MessageAction, URIAction],
                 image_url: str = None):
        if not action.json['label']:
            raise ValueError(f"\n\n[🔎 Check] Missing `label` parameter for `New.{type(action).__name__}`\n")
        self.json = {"type": "action", "action": action.json}


class QuickReply(object):
    """
Represents a Quick Reply Object.

Parameters
----------
items: List[New.QuickReplyButton]
    A list of QuickReply buttons. Should be `QuickReplyButton` objects.

Resources
---------
[LINE API Docs](https://developers.line.biz/en/reference/messaging-api/#quick-reply)
    """

    def __init__(self, items: List[QuickReplyButton]):
        if not isinstance(items, list):
            items = [items]
        for i in range(len(items)):
            items[i] = items[i].json
        print(items)
        self.json = {"items": items}


class Sender(object):
    """
    When sending a message from the LINE Official Account, you can specify the sender name, and their icon URL.

    Parameters
    ----------
    name : str

        Display name. Certain words such as `LINE` may **NOT** be used.
        Max character limit: 20

    icon_url : str
    
        URL of the image to display as an icon when sending a message.
        - Max character limit: 2000
        - URL scheme: https
        - Image format: PNG
        - Aspect ratio: 1:1
        - Data size: Up to 1 MB
    """

    def __init__(self, name: str = None, icon_url: str = None):
        self.json = {"name": name, "iconUrl": icon_url}


class TextMessage(object):
    """
    Creates a new Text Message.
    ## Parameters
    text : str
    
        The text.

        **Example for inserting emojis**
        
        *Method 1*
        ```py
        TextMessage("here's an emoji: {PRODUCT_ID:EMOJI_ID}")
        ```

        *Method 2*
        ```py
        TextMessage("here's an emoji: $", emojis=[ New.Emoji("PRODUCT_ID", "EMOJI_ID") ])
        ```

    emojis : List[Emoji]
    
        List of emojis.<br>e.g. `[ New.Emoji('product_id', 'emoji_id') ]`

    quick_reply : QuickReply
    
        Quick reply buttons that'll display on the bottom of the chat screen.

        ```py
        New.QuickReply([
            New.QuickReplyButton(action=...) # simple!
        ])
        ```

    sender : Sender

        The sender information for webhook.

        ```py
        New.Sender(...)
        ```
    """

    def __init__(self,
                 text: str,
                 emojis: List[Emoji] = None,
                 quick_reply: QuickReply = None,
                 sender: Sender = None):
        _EMOJIS = None
        if emojis:
            _EMOJIS = []
            if "$" in text:
                cur = 0
                for i in re.finditer("\$", text):
                    index = i.start()
                    js = emojis[cur].json
                    js['index'] = index
                    _EMOJIS.append(js)
                    cur += 1

            else:
                Logger.warning(
                    "[LINELIB] Warning:\nYou might forgot to put the keyword `$` inside your `text` to use emojis.\nFor example, `$ my text` => `( Line Emoji ) my text`\nRead more: https://developers.line.biz/en/reference/messaging-api/#text-message\n\n"
                )
        self.json = {
            "type": "text",
            "text": text,
            "emojis": _EMOJIS,
            "quickReply":
            getattr(quick_reply, "json") if quick_reply else None,
            "sender": getattr(sender, "json") if sender else None
        }

class VideoMessage:
    """
    LINE Video Message.
    ### Info: Video Aspect Ratio
    - A very wide or tall video may be cropped when played in some environments.
    
    - The aspect ratio of the video specified in originalContentUrl and the preview image specified in previewImageUrl should be the same. If the aspect ratio is different, a preview image will appear behind the video.
    
    ![video aspect ratio](https://developers.line.biz/assets/img/image-overlapping-en.0e89fa18.png)

    ## Parameters
    original_content_url : str
    
        The origianl content URL, should be MP4

    preview_image_url : str

        The preview image, should be JPEG or PNG.

    tracking_id : str = None
    
        ID used to identify the video when Video viewing complete event occurs. If you send a video message with `tracking_id` added, the video viewing complete event occurs when the user finishes watching the video
    """
    def __init__(self, original_content_url: str, preview_image_url: str, tracking_id: str = None):
        self.json = {
            "type": "video",
            "originalContentUrl": original_content_url,
            "previewImageUrl": preview_image_url,
            "trackingId": tracking_id
        }

class AudioMessage:
    """
    An audio message.

    original_content_url : str
    
        URL of audio file (Max character limit: 2000, M4A)

    duration : ms
    
        Audio duration. (In mileseconds)
    """
    def __init__(self, original_content_url: str, duration: ms):
        self.json = {
            "type": "audio",
            "originalContentUrl": original_content_url,
            "duration": dutation
        }

class LocationMessage:
    """
    Location message.

    title : str
    
        The title. e.g. my location

    address : str

        Address. e.g. 1-6-1 Yotsuya, Shinjuku-ku, Tokyo, 160-0004, Japan

    latitude : float

        Latitude. e.g. 35.687574

    longitude : float

        Longitude. e.g. 139.72922
    """
    def __init__(self, title: str, address: str, latitude: float, longitude: float):
        self.json = {
            "type": "location",
            "title": title,
            "address": address,
            "latitude": latitude,
            "longitude": longitude
        }

class TemplateMessage:
    """
    Template messages are messages with predefined layouts which you can customize.

    alt_text : str

    Alternative text. For example: `My trmplate message`

    json : dict
    
        Loads the Template from JSON.

    ## Examples
    
    ### Buttons
    ```py
    TemplateMessage("you have a message!",
    {
    "type": "buttons",
    "thumbnailImageUrl": "https://example.com/bot/images/image.jpg",
    "imageAspectRatio": "rectangle",
    "imageSize": "cover",
    "imageBackgroundColor": "#FFFFFF",
    "title": "Menu",
    "text": "Please select",
    "defaultAction": {
      "type": "uri",
      "label": "View detail",
      "uri": "http://example.com/page/123"
    },
    "actions": [
      {
        "type": "postback",
        "label": "Buy",
        "data": "action=buy&itemid=123"
      },
      {
        "type": "postback",
        "label": "Add to cart",
        "data": "action=add&itemid=123"
      },
      {
        "type": "uri",
        "label": "View detail",
        "uri": "http://example.com/page/123"
      }
    ]
  })
    ```
    
    ### Confirm
    ```py
    TemplateMessage("you have a message!", {
    "type": "confirm",
    "text": "Are you sure?",
    "actions": [
      {
        "type": "message",
        "label": "Yes",
        "text": "yes"
      },
      {
        "type": "message",
        "label": "No",
        "text": "no"
      }
      ]
    })
    ```
    
    ***
    
    ...See [this page](https://developers.line.biz/en/reference/messaging-api/#template-messages) for more *official* template examples by LINE Developers Documentation.
    """
    def __init__(self, alt_text: str, json: dict):
        self.json = {
            "type": "template",
            "altText": alt_text,
            "template": json
        }

class New:
    """
    Create a new `Text`, `Flex Message`, `Video Message`, and MORE!
    """
    Emoji = Emoji
    PostbackAction = PostbackAction
    QuickReplyButton = QuickReplyButton
    QuickReply = QuickReply
    Sender = Sender
    TextMessage = TextMessage
    MessageAction = MessageAction
    URIAction = URIAction
    DateTimePickerAction = DateTimePickerAction
    CameraAction = CameraAction
    CameraRollAction = CameraRollAction
    StickerMessage = StickerMessage
    ImageMessage = ImageMessage
    AudioMessage = AudioMessage
    VideoMessage = VideoMessage
    LocationMessage = LocationMessage
    TemplateMessage = TemplateMessage
