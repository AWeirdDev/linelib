"""
useless tools.
"""
from typing import Literal, List

# Long << str
class _Long(object):
    def __lshift__(self, t: type):
        if t in ['str', str]:
            class long_str(object):
                pass
            
            return long_str
            
Long = _Long()


# function(...) -> NoExecute("command")
class NoExecute:
    """
    Tells linelib not to execute the specified command.
    ```py
    NoExecute([
      "command"
    ])
    ```
    ## Parameters
    no_exec : List[..., Literal["command", "cog"]]
        What not to execute next, in an array (`list`).

    ## Valid Strings
    `command`: Normal commands that are registered with `@client.command`.
    `cog`: Cogs that are registered, and loaded with the following:
    ```py
    class MyCog(client.Commands, prefix="~"):
      ... # commands
    client.load_commands(MyCog) # loaded
    ```
    """
    def __init__(self, no_exec: List[
        Literal["command", "cog"]
    ]) -> None:
        self.ne = self.NO_EXEC = no_exec

    @property
    def is_valid(self):
        """
        Check if this is a valid feature in `LINELIB`. If so, returns `True`.

        **NOTE**

        Remember, this feature might be removed on next versions. However, you can still use the `NoExecute` at the moment.
        """
        # this is still in BETA
        # i will probably remove this feature
        return False
