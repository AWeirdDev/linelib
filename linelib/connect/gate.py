# Named http.

from __future__ import annotations

from ..exceptions import ClientException

import httpx # pip install httpx

def url(r: str):
  return "https://api.line.me/v2/" + r.replace('.', '/')

async def reply(client: type, rt: str, msgs: list, disabled: bool) -> None:
  try:
    async with httpx.AsyncClient() as session:
      r = await session.post(url('bot.message.reply'), headers=client.headers, json={
        "replyToken": rt,
        "messages": msgs,
        "notificationDisabled": disabled
      })
      print(r)
      return r
  except Exception as err:
    raise ClientException(err)
