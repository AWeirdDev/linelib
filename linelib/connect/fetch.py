"""
fetch fetch fetch fetch
"""

from __future__ import annotations
import httpx # pip install httpx

def fetch_this(thing: str):
  return "https://api.line.me/v2/bot/" + thing.replace('.', '/')

async def profile(headers: dict, user_id: str) -> type:
  async with httpx.AsyncClient() as session:
    res = await session.get(fetch_this(f'profile.{user_id}'), headers=headers) # response
    json = res.json() # the response json
    class Profile:
      name = display_name = json['displayName']
      id = user_id = json['userId']
      language = region = json['language']
      picture_url = picture = avatar_url = avatar = json['pictureUrl']
      status_message = status = json['statusMessage']
      
    return Profile() # without brackets...? well, it works too.