import base64
import hashlib
import hmac

from ..errors import InvalidSignature
from ..models.message import WebhookTextMessage, WebhookLocationMessage, WebhookPostback, WebhookVideoMessage, WebhookStickerMessage
from ..database import db


class SignatureValidator(object):
    """
    https://developers.line.biz/en/reference/messaging-api/#signature-validation
    """
    def __init__(self, channel_secret):
        self.channel_secret = channel_secret

    def validate(self, body: str, signature: str):
        r"""
        Checks signature.
        
        :param str body: Request body as text.
        :param str signature: X-Line-Signature value (as text again).
        """
        hash = hmac.new(self.channel_secret.encode('utf-8'),
            body.encode('utf-8'), hashlib.sha256).digest()
        try:
            return hmac.compare_digest(signature.encode("utf-8"), base64.b64encode(hash))
        except:
            raise BaseException('\nOh no... This is bad. The HMAC module has no \'compare_digest\' function.')


def ParseEvent(req: dict, CAT: str):
        e = req["events"][0] # event
        args = (req, CAT)
             
        if e["type"] == "message":
            return {
                "text": WebhookTextMessage,
                "location": WebhookLocationMessage,
                "video": WebhookVideoMessage,
                "sticker": WebhookStickerMessage
            }[
              e["message"]["type"]
            ](req, CAT)
            # lazy coding
                
        elif e['type'] == "postback":
            wpb = WebhookPostback(req, CAT)
            process_id = wpb.data
            db.handlers[process_id](wpb)
            return wpb

        
