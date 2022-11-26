from linelib import Client

cmd = Client.Commands.cmd

class MyCog(
    Client.Commands,
    prefix="!",
    # storage:
    my_str="shared string!",
    PROTECTED_secret="shhh... this is a secret" # unwritable, or removable 
  ):
    @cmd(name="secrets", my_str2="local string!")
    def secrets(ctx):
        storage = ctx.storage
        all_secrets = [
            storage.shared.my_str,
            storage.shared.protected.secret, # PROTECTED_secret
            storage.local.my_str2
        ]
        ctx.reply("Here are my secrets:\n" + "\n".join(all_secrets))
