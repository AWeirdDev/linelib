"""
fetch fetch fetch fetch
"""

from __future__ import annotations
import httpx # pip install httpx
import termcolor
import uuid
import os
from tqdm import tqdm
from mimetypes import guess_extension

from ..exceptions import ClientException


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

async def profileAndGroup(headers: dict, user_id: str, group_id: str) -> type:
    async with httpx.AsyncClient() as session:
        res = await session.get(fetch_this(f'profile.{user_id}'), headers=headers) # response
        json = res.json() # the response json
        
        class Profile:
          name = display_name = json['displayName']
          id = user_id = json['userId']
          language = region = json['language']
          picture_url = picture = avatar_url = avatar = json['pictureUrl']
          status_message = status = json['statusMessage']

        async def get_group():
            async with httpx.AsyncClient() as session:
                GS_RES = await session.get(fetch_this(f'group.{group_id}.summary'), headers=headers)
                groupSum = GS_RES.json()

                MC_RES = await session.get(fetch_this(f'group.{group_id}.members.count'), headers=headers)
                groupMemberCount = MC_RES.json()['count']
        
                
                class Group:
                    count: int = groupMemberCount
                    id: str = groupSum['groupId']
                    name: str = groupSum['groupName']
                    picture_url = picture = groupSum['pictureUrl']

                    async def leave(self):
                        return await leave_gr(headers, group_id)

                return Group()

        return (Profile(), get_group)

async def leave_gr(headers: dict, group_id: str):
    """
    Leave a `gr`oup chat.
    """
    try:
        async with httpx.AsyncClient() as session:
            res = await session.post(fetch_this(f'group.{group_id}.leave'), headers=headers)
            return res
    except Exception as err:
        raise ClientException(err)


async def getContent(headers: dict, message_id: str):
    """
    Fetches the message content. (images, videos, audio, and files)
    """
    fileName = "linelib-dl-" + str(uuid.uuid4()).split('-')[0] + ".TMP"
    try:
        client = httpx.AsyncClient()
        with open(fileName, 'wb') as file: # FILE !important
            async with client.stream('GET', f"https://api-data.line.me/v2/bot/message/{message_id}/content", headers=headers) as response:
                print("\n\n" + termcolor.colored('linelib v2', 'light_green') + "- 📦 Downloading files...")
                
                fileExtension = guess_extension(response.headers['content-type'].partition(';')[0].strip())
                total = int(response.headers["Content-Length"])
                with tqdm(total=total, unit_scale=True, unit_divisor=1024, unit="file") as progress:
                    num_bytes_downloaded = response.num_bytes_downloaded
                    async for chunk in response.aiter_bytes():
                        file.write(chunk)
                        progress.update(response.num_bytes_downloaded - num_bytes_downloaded)
                        num_bytes_downloaded = response.num_bytes_downloaded

                print(termcolor.colored('linelib v2', 'light_green') + ' - Finished!\n') # finished
                
                file.close()
                # .TMP => length: 4
                newName: str = fileName[:-4] + "." + fileExtension
                os.rename(fileName, newName)
                return newName
    
    except Exception as err:
        raise ClientException(err)