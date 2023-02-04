from __future__ import annotations

import inspect
from typing import Callable

from ..exceptions import MissingArgument, Async
from .rule import CommandRule, DEFAULT_RULE, _dfr

class _str:
    def __matmul__(self, other):
        return str

String = _str()

VALID_TYPES = [int, float, bool, str]

class Cog:
    name = "UnnamedCog"
    show_not_found_log = False # whether to show the not found log.
    
    def __init__(self):
        self._ll_CONSTRUCTED = True

    def __init_subclass__(cls) -> None:
        # ll => linelib
        cls._ll_commands: list = []
        cls._ll_CONSTRUCTED: bool = False
        [cls._ll_commands.append(getattr(cls, i)) if (not i.startswith('__')) and (isinstance(getattr(cls, i), CogCommandWrapper)) else None for i in dir(cls)]

    async def emit(self, ctx: type):
        gathered = []
        
        for cmd in self._ll_commands:
            res = await cmd.emit(self, ctx)
            gathered.append(res)

        if all(i == 'no' for i in gathered):
            await self.not_found(ctx, ctx.content.strip().split(' ')[0])
            return 'all-nf' # all not found

    async def not_found(self, ctx, command: str):
        """
        Do something when a command was not found.
        """
        pass # default

class CogCommandWrapper:
    """
    Represents a cog command.
    """
    def __init__(self, cmd_name: str, func, rule: CommandRule | _dfr = DEFAULT_RULE):
        parameters = inspect.signature(func).parameters

        self.ann = []
        self.rule = rule.emit

        keywordOnlyAlreadyFound = False
        cur = 0 # current state

        for name, param in parameters.items():
            cur += 1
            if cur < 3: # meaning that (1, 2) will both be ignored
                continue # ignore

            if (not param.annotation in VALID_TYPES) and (not param.annotation is inspect._empty):
                raise TypeError(f'The type \'{param.annotation.__name__}\' could not be recognized as a valid type.\nLinelib only accepts the following:\nint, float, bool, str')

            if param.kind == inspect.Parameter.KEYWORD_ONLY:
                if keywordOnlyAlreadyFound:
                    raise TypeError('\n\nThe keyword (*) should only be used once in function arguments. This represents that rest of the string that\'s sent from the user will all be passed into this parameter.\n\n')
                else:
                    keywordOnlyAlreadyFound = True
                    # str(name) == parameter name.
                    self.ann.append(('*', str(name)))
            else:
                ann = param.annotation if (not param.annotation is inspect._empty is inspect._empty) else str # empty annotation? then str.

                self.ann.append((ann,))

        self.func: type = func
        self.name = cmd_name
    
    async def emit(self, o: Cog, ctx: type):
        """Emits the command."""

        msg = ctx.content.strip()

        splitted = msg.split(' ')
        
        args = splitted[1:]

        if splitted[0] == self.name:
            should = self.rule(ctx)
            if not should: # not allowed
                await self._RULE_REJECT(o, ctx)
                return
            _PASS = [] # arguments that will be passed in. (*)
            _NAMED = {} # named arguments. (**)

            for i in range(len(args)):
                if (i + 1) > len(self.ann):
                    break # end this
                if self.ann[i][0] != '*':
                    try:
                        _PASS.append(self.ann[i][0](args[i])) # annotations (type)
                    except Exception as err:
                        await self._LL_ERR(o, ctx, err)
                else: # *
                    _NAMED[self.ann[i][1]] = ' '.join(args[i:])
            try:
              await self.func(o, ctx, *_PASS, **_NAMED)
            except Exception as err:
                ERROR = MissingArgument(str(err)) if (isinstance(err, TypeError) and "missing" in str(err)) else err
                await self._LL_ERR(o, ctx, ERROR)

        return 'no'

    def on_error(self, function: Callable) -> Callable:
        if not inspect.iscoroutinefunction(function):
            raise Async("Async Function", f"The function '{function.__name__}' should be an async (coroutine) function. Example:\n\nasync def my_function(...)\n\n")

        self._LL_ERR = function
        return function

    def rule_reject(self, function: Callable) -> Callable:
        if not inspect.iscoroutinefunction(function):
            raise Async("Async Function", f"The function '{function.__name__}' should be an async (coroutine) function. Example:\n\nasync def my_function(...)\n\n")

        self._RULE_REJECT = function
        return function

    async def _RULE_REJECT(self, ctx):
        pass # default

    
    async def _LL_ERR(self, o, ctx, err):
        raise err # default


def cog_command(*, name: String@CogCommandWrapper, rule: CommandRule = DEFAULT_RULE) -> CogCommandWrapper:
    """
    Registers a cog command.
    """
    def wrapper(func):
        if not inspect.iscoroutinefunction(func):
            raise Async("Async Function", f"The function '{func.__name__}' should be an async (coroutine) function. Example:\n\nasync def my_function(...)\n\n")
        return CogCommandWrapper(name, func, rule)

    return wrapper

cog_cmd = cog_command # ~ createAlias