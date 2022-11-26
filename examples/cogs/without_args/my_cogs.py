# My Cogs!
from linelib import Client

cmd = Client.Commands.cmd

class MyCog(Client.Commands, prefix="!"):
  @cmd(name="ping")
  def ping(ctx):
    ctx.reply([ # send multiple messages
        "Pong!",
        f"LINE API Ping: {ctx.client.ping}"
    ])
