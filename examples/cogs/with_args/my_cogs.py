from linelib import Client, Long

cmd = Client.Commands.cmd

class MyCog(Client.Commands, prefix="!"):
  @cmd(name="drink")
  def drink(ctx, times: int, reason: Long << str = "no reason"):
    # Use 'Long << str' for long strings like a sentence,
    # Otherwise your sentence might be cut.
    # Example without Long: "this is important" becomes "this"
    ctx.reply(f"You drank water {times} times.\nReason: {reason}")
