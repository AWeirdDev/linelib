from linelib import Client, Long

cmd = Client.Commands.cmd

class MyCog(Client.Commands, prefix="!"):
  @cmd(name="drink")
  def drink(ctx, times: int, reason: Long << str = "no reason"):
    ctx.reply(f"You drank water {times} times.\nReason: {reason}")
