"""\
LINELIB sample bot.

Features included:
- Bot ready log

(c) 2022 AWeirdDev (AWeirdScratcher)
"""

import logging

from linelib import Client

client = Client("channel secret", "access token")

@client.event("ready")
def ready():
  print(f"I'm ready! Ping: {client.ping}")

client.run(
  host="0.0.0.0", 
  port=8080,
  LOG_LEVEL=logging.ERROR # make things clear
)
