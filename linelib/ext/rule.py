from __future__ import annotations

from typing import Literal
import time

from ..tmp import Tmp

# const
VALID_RULES = {
    # tuple: low usage.
    "cooldown": ('seconds',), 
    "except": ('users',), 
    "for": ('users',),
    "based.custom": (),
    "usage_limit": ('times',)
}

class _dfr:
    def emit(self, *args, **kwargs) -> bool:
        return True

# export
DEFAULT_RULE = _dfr()

# export
class CommandRule:
    """
    Represents a command rule. The specification depends on the rule type.

    ## cooldown
    Represents a command cooldown. The user should wait until the cooldown (in seconds) ends, or else a specific command will not work.

    > Arg Requires: `seconds: int`

    ```py
    CommandRule(
      rule='cooldown',
      seconds=10
    )
    ```

    ## except
    Run the command except for someone. The specified users will not be able to use the command. An array of user ids (string) should be passed.

    > Arg Requires: `users: list[str]`

    ```py
    CommandRule(
      rule='except',
      users=[
        'user id 1',
        'user id 2'
      ]
    )
    ```

    ## for
    Run the command for some people. The users that are not on the list will not be able to use this command. An array of user ids (string) should be passed.

    > Arg Requires: `users: list[str]`

    ```py
    CommandRule(
      rule='for',
      users=[
        'user id 1',
        'user id 2'
      ]
    )
    ```

    ## based.custom
    Based on your custom rule. Linelib will not touch anything from your function.

    > Arg Requires: No additional arguments required for this condition.

    ```py
    class MyRule(CommandRule):
      def handler(self, ctx):
        return True # true or false

    MyRule(rule='based.custom') # now it's a valid rule.
    ```

    ## usage_limit
    Limit a command based on the usage of it. For instance, using a usage limitation for each user, everyone will only be able to use it for a specified time.

    > Arg Requires: `times: int`

    ```py
    # the command could only be used once
    
    CommandRule(
      rule='usage_limit',
      times=1
    )
    ```
    """
    rule: str

    def __init__(self, *, rule: Literal["cooldown", "except", "for", "based.custom", "usage_limit"], **variations):
        if not rule in VALID_RULES:
            raise ValueError(f"\n\nThe rule type '{rule}' does not exist. Consider checking your spelling.\nHere's a complete list of valid rules for your reference:\n\n{', '.join(VALID_RULES)}")

        if not all(arg in variations for arg in VALID_RULES[rule]):
            raise ValueError(f'\n\nSeems like you might have forgotten to pass in some arguments for the command rule \'{rule}\'. This requires the following arguments to be passed:\n\n{", ".join(VALID_RULES[rule])}\n\n')

        self.rule_str = rule
        self.kwargs = variations

    def __init_subclass__(cls):
        """
        A custom rule subclass init method.

        Example:
        
        ```py
        class MyRule(CommandRule):
          def handler(self, ctx):
            return True # true or false
    
        MyRule(rule="based.custom") # now it's a valid rule.
        ```
        """
        cls.rule_str = 'based.custom'

    def emit(self, ctx) -> bool:
        return {
            "based.custom": self.handler,
            "cooldown": self.cooldown,
            "except": self._except,
            "for": self._for,
            "usage_limit": self.usage_limit
        }[self.rule_str](ctx)

    def handler(self, ctx) -> bool:
        return True # default, rewritable.
    
    def cooldown(self, ctx) -> bool:
        AUTHOR_ID = ctx.author.id
        
        status: int | None = Tmp.rule_cooldown.get(AUTHOR_ID, None)
        if not status:
            Tmp.rule_cooldown[AUTHOR_ID] = time.time()
            print(Tmp.rule_cooldown)
            return True

        result: bool = (time.time() - status) >= self.kwargs['seconds']

        if result: # if True:
            Tmp.rule_cooldown[AUTHOR_ID] = time.time() # reset
        
        return result

    def _except(self, ctx) -> bool:
        return not ctx.author.id in self.kwargs['users']

    def _for(self, ctx) -> bool:
        return ctx.author.id in self.kwargs['users']

    def usage_limit(self, ctx) -> bool:
        AUTHOR_ID = ctx.author.id
        status = Tmp.rule_usage.get(AUTHOR_ID, None) # times

        if not status:
            Tmp.rule_usage[AUTHOR_ID] = 1

            return True # passed!

        if status > self.kwargs['times']:
            return False # impossible...

        # else: (IGNORE)
        Tmp.rule_usage[AUTHOR_ID] += 1

        return True

