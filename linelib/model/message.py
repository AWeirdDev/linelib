from __future__ import annotations

class WBTextMessage:
  def __init__(self, req: dict) -> WBTextMessage:
    self.req = req['message']

  @property
  def content(self):
    return self.req['text']

  text = content

  @property
  def id(self):
    return self.req['id']


class WBPostback:
  def __init__(self, req: dict) -> WBPostback:
    self.req = req['postback']
    self.TYPE = 'postback'

  @property
  def data(self):
    return self.req['data']

  @property
  def datetime(self):
    res = self.req.get('params', {"datetime": None}).get('datetime')
    if res:
      self.TYPE = 'datetime'
    return res

  @property
  def rich_menu(self):
    if self.TYPE != 'postback':
      rm = self.req.get('params', {
        # NOT FOUND value (default value)
        "newRichMenuAliasId": None,
        "status": None
      })
      class RichMenuSwitchEvent:
        status: str = rm['status']
        new_rich_menu_alias_id = new_rich_menu = rm['newRichMenuAliasId']
  
      res = RichMenuSwitchEvent()
      if res.new_rich_menu_alias_id:
        self.TYPE = 'rich_menu_switch'
      return res
    return None


# bro think he smart :skull: