from linelib import Client
from my_cogs import MyCog

client = Client("secret", "token")
client.load_commands(MyCog)

@client.event("ready")
def r():
  print("Ready! Ping: %i" % client.ping)

client.run(host="0.0.0.0", port=8080)
