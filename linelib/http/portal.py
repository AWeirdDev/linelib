"""\

🌀 Opens the magic portal for webhooks.<br>
***
Required Package: `flask`<br>
`pip install flask`

"""
import logging
import flask
import requests
import inspect

import time as TIME
from flask import Flask  # type: ignore
from typing import Literal, Union
from threading import Thread
from uuid import uuid4
from inspect import isclass

from ..const import DEFAULT
from .webhook import SignatureValidator, ParseEvent
from ..logger import Logger
from ..errors import InvalidSignature, CalculationNotReady, OutOfService, Unsupported, lineApiError
from ..models.types import ms, Count, Demographics
from ..models.message import WebhookTextMessage

# const
SUP = ["int", "float", "bool", "str"]
BUILTIN = ["linelib.tools._Long.__lshift__.<locals>.long_str"]


class UseDevServer:
    r"""
    Uses a Dev Server for testing, and checking your host URL<br>`replit.com` is recommended.

    :param str host: Host
    :param int port: Port
    :param LOG_LEVEL: *Optional* The logging Log Level for the `flask` app.
    """

    def __init__(self,
                 host: str = DEFAULT.portal.host,
                 port: int = DEFAULT.portal.port,
                 LOG_LEVEL=logging.DEBUG):
        Logger.info("[LINELIB] Using `dev-server` as development server.\n")

        log = logging.getLogger("werkzeug")
        log.setLevel(LOG_LEVEL)  # Only errors will be printed. Yeah somehow...
        app = Flask("Dev Server".replace(" ", "-").lower())

        @app.route("/")
        def index():
            return DEFAULT.STATIC.UDS_HTML

        app.run(host=host, port=port)


UseTestServer = UseDevServer


class Client:
    """
    Represents a hosting server.<br>Use the `handle` function to parse signatures.

    :param str channel_secret: The channel secret for the `handler`.
    :param str channel_access_token: Channel access token for the client (bot).
    :param bool default_handler: Use the default handler? (RECOMMENDED)
    :param str prefix: Command prefix (Optional)
    """

    def __init__(self,
                 channel_secret: str,
                 channel_access_token: str,
                 default_handler: bool = True,
                 prefix: str = None):
        self.channel_secret = channel_secret
        self.channel_access_token = self.CAT = channel_access_token
        self.app = Flask("linelib")
        self.when = {
            "text": None,
            "location": None,
            "ready": None,
            "postback": None,
            "image": None,
            "video": None,
            "sticker": None
        }
        self.ready = False
        self.commandsEmit = []
        self.prefix = prefix
        #self.shouldnt = []

        def handler():
            r"""
            Uses the LineLib default webhook handler. The route will be `/webhook` after using it.
            """
            Logger.debug(
                "\033[92m[LINELIB]\033[0m Using LineLib default webhook handler.\n\033[31m*  [WARN] The `/webhook` route is for line webhooks. Use it for your bot settings.\033[0m\n\033[96m*  [💡TIP] You could use the `UseDevServer` class to test out your server.\033[0m\n\n"
            )

            @self.app.route("/webhook", methods=['GET', 'POST'])
            def webhook_handler():
                res = self.handle(flask.request)
                SN = "\n"
                if not res:
                    raise InvalidSignature(
                        f"\nFailed to process the following request:{SN}{SN}{flask.request.get_data(as_text=True) or f'(* BLANK_REQUEST *){SN}* It was probably caused by: it was a user'}\n\n"
                    )
                req = flask.request.json
                ignore = False
                try:
                    req["events"][0]
                except:
                    print("Done verifying.")
                    ignore = True
                if not ignore:
                  if req['events'][0]['type'] == "message":
                    TYPE = req['events'][0]['message']['type']
                  elif req['events'][0]['type'] == "postback":
                    TYPE = "postback"

                  e = ParseEvent(req, self.channel_access_token)
                #print(req)
                  if TYPE == "text":
                      self._go_over_cmds(e)
                  self._trigger(TYPE, ctx=e)
                return "OK"

        # handler end
        self.app.useLineLibHandler = handler
        self.useLineLibHandler = handler
        if default_handler: handler()

    def _go_over_cmds(self, e):
        for i in self.commandsEmit:
            e.client = self # UNSAFE.
            i(e)

    def handle(self,
               request: flask.request) -> flask.Response:  # might might not
        """
        Parse signatures. If it's valid, will call the events as well

        :param flask.request request: A flask request object. (REQUIRED)
        """
        if request.method == 'POST':
            signature = request.headers['X-Line-Signature']
            body = request.get_data(as_text=True)  # good i think
            result = SignatureValidator(self.channel_secret).validate(
                body, signature)
            return result
        else:
            return False

    def event(self, name: Literal["text", "location", "ready", "postback", "image", "video", "sticker"]):
        """
        Listen to events.
        
        ## Example Usage
        ```py
        @event("ready")
        def ready() -> None:
            print("I am ready!")
        ```
        """
        acc = list(self.when.keys())
        if not name in acc:
            ps = "• " + "\n• ".join(acc)
            raise ValueError(
                f"\n\n[WARN] Unknown event name: `{name}`, it should be one of the following:\n{ps}\n\n"
            )

        def wrapper(e, *args, **kwargs):
            if (not "ctx" in e.__code__.co_varnames) and (name != "ready"):
                Logger.warning(
                    f"\n\n[WARNING] You did not add the required argument — `ctx` — in your function ('{e.__name__}' at {hex(id(e))})\nIn addition, you might receive an error while the event was triggered and sent to your handler.\n\n"
                )
            self.when[name] = e
            return e

        return wrapper

    def _trigger(self, event: str, *args, **kwargs):
        if self.when[event]:
            self.when[event](**kwargs)


    def run(self,
            /,
            host: str = DEFAULT.portal.host,
            port: int = DEFAULT.portal.port,
            LOG_LEVEL=logging.DEBUG,
            *args,
            **kwargs):
        """
        Starts the bot.
        ## Parameters
        host : str = `DEFAULT.portal.host`
            The host.

        port : str = `DEFAULT.portal.port`
            The port.

        LOG_LEVEL = `logging.DEBUG`
            `werkzeug` logger level. By setting it to `logging.ERROR` could mute most INFO messages. (They're really annoying!)

        *args, **kwargs
            Positional arguments, for instance: `threaded=True`. Will be parsed to the `flask.Flask.run` function. Here's how we parsed it:
            ```py
            app.run(host=host, port=port, **kwargs) # your positional arguments
            ```
        """
        log = logging.getLogger("werkzeug")
        log.setLevel(LOG_LEVEL)
        Logger.info("\033[0mStarting Client..")

        @self.app.before_first_request
        def beforeFirst(*args, **kwargs): # i do not know the arguments
            self.ready = True
            Logger.info("\n\033[94m🎉 First request — We Made It!\n\033[0m")
            self._trigger("ready")

        def HPCheck():
            Logger.info("\n\033[94m✨ Checking server status...\n\033[0m")
            TIME.sleep(5)
            Logger.info(
                "\n\033[0m[ 🚀 Please Wait ] Time passed: 5sec after launching "
            ) if not self.ready else None
            TIME.sleep(5)
            if not self.ready:
                Logger.warn(
                    "\n[WARN] It has been 10 seconds since the app started. However, we seemed to be not receiving any requests from your browser.\nIt's because you are not using it, OR the host / port is incorrect.\nIf so, you can configure them in the `Client.run` function.\nEx.\n \033[94mrun\033[0m(host=\033[93m'0.0.0.0'\033[0m, port=\033[92m8080\033[0m) \033[96m# http\033[0m\n"
                )

        Thread(target=HPCheck).start()
        self.app.run(host=host, port=port, **kwargs)

    class Commands():
        """
        See `__init_subclass__` for more.
        """
        def __init__(self, client) -> None:
            self.client = client
        def __init_subclass__(cls,
                              prefix: str = "",
                              load_desc: bool = True,
                              *sharedStorageArgs,
                              **sharedStorageKwargs):
            """
        # Client.Commands
        Commands parent class.
        [Usage](#Example-Usage) and [Subclass Params](#SubClass-Parameters)
        ## Example Usage
        ```py
        class MyCommands(Commands, prefix = "!", PROTECTED_hey = "I'm thankful"):
            @Commands.command(name = "simple")
            def simple(ctx):
                \"\"\"\\
                A really simple command!
                \"\"\"
                string = ctx.sharedStorage.protected.hey
                ctx.reply("hey, thanks for caring me, %s ;)" % string)
        ```
        ## SubClass Parameters
        prefix : str = ""
            The command prefix. Left blank by default.

        load_desc : bool = True
            "Load Description?" in short. It means whether load the `__doc__` attribute from your commands or not.

        ## Notes
        To load a command cog (`Client.Commands`), use the `Client.load_cog` or `client.load_commands` function.
        ```py
        client.load_cog(MyCommandCog)
        # OR
        client.load_commands(MyCommandCog)
        ```
        """
            cls.prefix = prefix
            supported = {}
            for i in sharedStorageKwargs:
                if i.startswith("PROTECTED_"):
                    supported[i.replace("PROTECTED_", "",
                                        1)] = sharedStorageKwargs[i]

            class SharedStorage:
                pass

            class protected(object):

                def __getattr__(self, key):
                    return supported[key]

                def __setattr__(self, *args, **kwargs):
                    raise AttributeError(
                        "can't set attribute (linelib.protected)")

                def __delattr__(self, *args, **kwargs):
                    raise AttributeError(
                        "can't delete attribute (linelib.protected)")

            SharedStorage.protected = protected()

            if "protected" in sharedStorageKwargs:  # set
                raise TypeError(
                    "\n\nThough should not add `protected` storage key. If you want this to be protected, try using `PROTECTED_` as prefix for your args to make it protected.\n\n"
                )
            for i in sharedStorageKwargs:
                if not i.startswith("PROTECTED_"):
                    setattr(SharedStorage, i, sharedStorageKwargs[i])

            cls.shared = SharedStorage

            COMMANDS = {}

            for i in dir(cls):
                #print(getattr(cls, i))
                if isclass(getattr(cls, i)) and (not i == "__class__") and (
                        not i in ["shared"]):
                    d = getattr(cls, i)
                    #print(d)
                    d.storage.shared = cls.shared
                    d.shared_storage = d.sharedStorage = cls.shared
                    COMMANDS[d.name] = d


            def TextEmitter(e):
                #print(COMMANDS)
                # the above is for debugging.
                if e.text.startswith(prefix):
                    if e.text.replace(prefix, "", 1).split(" ")[0] in COMMANDS:
                        # this is bad.
                        target = COMMANDS[e.text[len(prefix):].split(" ")[0]]
                        e.storage = target.storage
                        e.localStorage = target.localStorage
                        e.sharedStorage = target.sharedStorage
                        #e.client = cls.client
                        args = dict(target.args)
                        ohWow = {}
                        transform = {
                            "int": int,
                            "str": str,
                            "float": float,
                            "bool": bool
                        }
                        #e.text[len(prefix):]
                        #print(e.text[len(prefix):])
                        try:
                          _all = e.text[len(prefix):].split(" ", 1)[1].split()
                        except IndexError:
                            _all = ""
                        del args['ctx']
                        #print(_all)
                        for i in range(len(args)):
                            param = str(args[list(args.keys())[i]])
                            _t = param
                            argument = param.split(": ")[0]
                            if argument == "ctx":
                                continue
                            hasE = " = " in _t.split(": ")[1]
                            
                            if ": " in _t:
                                _t = _t.split(": ")[1].split(" = ")[0]
                            try:
                              if _t in transform:
                                  if transform[_t](_all[i]) != "":
                                    ohWow[argument] = transform[_t](_all[i])
                              else:
                                  if " ".join(_all[i:]) != "":
                                    ohWow[argument] = " ".join(_all[i:])
                            except Exception as err:
                                if not hasE: # no type specified && bad args
                                    if "on_error" in dir(target):
                                        return target.on_error(e, err)
                                    else:
                                        raise err
                        target.handler(e, **ohWow)  # function
                    else:
                        Logger.warn(
                            "[ ⚙️ | %s ] Command Not Found: " % cls.__name__ +
                            e.text[len(prefix):].split(" ")[0])  # find a smile here :]

            class Emitters:
                text = TextEmitter

            cls.emitter = Emitters

        # end main

        def command(name: str = None, *storageArgs, **storageKwargs):
            """
            Registers a command. It should be in a subclass.
            
            ## Example Usage
            ```py
            @Commands.command( name="yay", PROTECTED_secret="I like sleeping" )
            def best_command_ever(ctx):
                ctx.reply("Let me tell you my secret: " + ctx.localStorage.protected.secret)
            ```
            **❌ WRONG**
            ```py
            @Commands.command( ..., prefix="no!" )
            ...
            
            # Do not set prefixes like this!
            ```
            Set your prefix using subclass. See [linelib.Commands](https://www.youtube.com/watch?v=dQw4w9WgXcQ)
            
            
            ## Parameters
            
            name : str = None
                Command name.

            *storageArgs, **storageKwargs
            
                Optional arguments for the `localStorage`.
                
                **Example**

            ```py
            @Commands.command(..., mine="my secret string! hehe!")
            def func(ctx, ...params):
              print(ctx.storage.local.mine)
            ```
            """

            class LocalStorage:
                pass

            _name = name

            supported = {}
            for i in storageKwargs:
                if i.startswith("PROTECTED_"):
                    supported[i[10:]] = storageKwargs[i]

            class protected(object):

                def __getattr__(self, key):
                    return supported[key]

                def __setattr__(self, *args, **kwargs):
                    raise AttributeError(
                        "can't set attribute (linelib.protected)")

                def __delattr__(self, *args, **kwargs):
                    raise AttributeError(
                        "can't delete attribute (linelib.protected)")

            LocalStorage.protected = protected()

            if "protected" in storageKwargs:
                raise TypeError(
                    "\n\nThough should not add `protected` storage key. If you want this to be protected, try using `PROTECTED_` as prefix for your args to make it protected.\n\n"
                )

            for i in storageKwargs:
                setattr(LocalStorage, i, storageKwargs[i])

            def wrapper(func, *args, **kwargs):
                _args = inspect.signature(func).parameters

                cur = 0  # cur
                for i in _args:
                    if ":" in str(_args[i]):
                        if (not str(_args[i]).split(": ")[1] in SUP) and (
                                not str(_args[i]).split(": ")[1] in BUILTIN):
                            if (not " = " in str(_args[i]).split(": ")[1]):
                              raise Unsupported(
                                f"Unsupported type: {str(_args[i]).split(': ')[1]}"
                            )
                        if str(_args[i]).split(": ")[
                                1] in BUILTIN and cur != len(_args.keys()) - 1:
                            raise ValueError(
                                "\n\nERROR: You can only use `Long << str` as type in the **LAST** parameter. Putting it between arguments might cause errors.\n\n"
                            )
                    cur += 1

                class CMD:
                    handler = func
                    name = _name or func.__name__
                    args = _args

                    def error(error_type: Union[type, str] = None):
                        def wrapper(fn, *args, **kwargs):
                            def Emitter(ctx, err):
                                if error_type:
                                    if isinstance(err, str):
                                        check: bool = err.__name__ == error_type
                                    else:
                                        check: bool = type(err) == error_type

                                    if not check:
                                        raise err # raise it again

                                fn(ctx, err)
                            CMD.on_error = Emitter
                            return fn
                        return wrapper
                                        
                        

                    class storage:
                        local = LocalStorage

                    local_storage = localStorage = LocalStorage

                CMD.__name__ = "_" + str(uuid4()).replace("-", "_")

                return CMD

            return wrapper

        cmd = command

    def load_cog(self, Cog: type) -> None:
        # supported
        c = Cog(self)
        self.commandsEmit.append(c.emitter.text)
        return  # useless.

    load_commands = load_cog

    def command(self, name: str, prefix: str = None) -> type:
        prefix = (prefix or self.prefix) or ""
        _name = name

        def wrapper(func, *args, **kwargs):

            class Command:
                name = _name
                handler = func
                args = inspect.signature(func).parameters

            def TextEmitter(e):
                if e.text.startswith(prefix):
                    if e.text.replace(prefix, "", 1).split(" ")[0] == Command.name:
                        if e.text[len(prefix):] == Command.name:
                            Command.handler(e)
                    else:
                        Logger.warn("Command Not Found: " +
                                    e.text[len(prefix):])

            class Emitters:
                text = TextEmitter

            Command.emitter = Emitters
            self.commandsEmit.append(Command.emitter.text)
            return Command

        return wrapper

    @property
    def ping(self) -> ms:
        """
        Get elapsed time via sending a request to the endpoint.

        **WARNING**: This might take a while to process!
        """
        return requests.get("https://api.line.me/v2/bot/info",
                            headers={
                                "Authorization": "Bearer " + self.CAT
                            }).elapsed.total_seconds() * 1000

    @property
    def _newHeader(self) -> dict:
        return {"Authorization": "Bearer " + self.CAT}

    def get_message(self, message_id: int):
        """
        Get Message.
        :param int message_id: Message ID.
        """
        return WebhookTextMessage(
            requests.get("https://api-data.line.me/v2/bot/message/%i/content" %
                         message_id,
                         headers=self._newHeader).json(), self.CAT)

    def message_deliveries(self, date: str) -> Count:
        """
        Returns the number of messages sent from LINE Official Account on a specified day.
        :param str date: The date. Format: `yyyyMMdd`, Timezone: `UTC+9`. (e.g. `20220101`, `20191011`, ...)
        """
        status = requests.get(
            "https://api.line.me/v2/bot/insight/message/delivery?date=%s" %
            date,
            headers=self._newHeader).json()
        if status['status'] == "unready":
            raise CalculationNotReady(
                "\n\n🧮 We haven't finished calculating the number of sent messages for the specified `date`. Try again later. Calculation usually takes about a day.\n"
            )
        elif status['status'] == "out_of_service":
            raise OutOfService(
                "\n\n❌ The specified `date` is earlier than the date on which we first started calculating sent messages."
            )

        wow = []

        def try_or_null(val):
            try:
                wow.append(status[val])
                return status[val]
            except:
                #wow.append(0)
                # it really doesn't matter if you add 0 or not.
                return 0

        class Count:
            json = status

        toAdd = [
            "broadcast", "targeting", "autoResponse", "welcomeResponse",
            "chat", "apiBroadcast", "apiPush", "apiMulticast", "apiNarrowcast",
            "apiReply"
        ]

        for i in toAdd:
            text = i
            if text[3].isupper():
                text = "api" + "_" + text[3].lower() + text[4:]
                #print(text)

            setattr(Count, text, try_or_null(i))

        Count.total = sum(wow)

        return Count

    def get_followers(self, date: str) -> Count:
        """
        Returns the number of users who have added the LINE Official Account on or before a specified date.
        :param str date: The date. Format: `yyyyMMdd`, Timezone: `UTC+9`. (e.g. `20220101`, `20191011`, ...)
        """
        res = status = requests.get(
            "https://api.line.me/v2/bot/insight/followers?date=%s" % date,
            headers=self._newHeader).json()
        if res['status'] == "unready":
            raise CalculationNotReady(
                "\n\n🧮 We haven't finished calculating followers for the specified `date`. Try again later. Calculation usually takes about a day."
            )
        elif res['status'] == "out_of_service":
            raise OutOfService(
                "\n\nThe specified `date` is earlier than the date on which we first started calculating followers"
            )

        wow = []

        def try_or_null(val):
            try:
                wow.append(status[val])
                return status[val]
            except:
                return 0

        class Count:
            json = status

        toAdd = ["followers", "targeted_reaches", "blocks"]

        for text in toAdd:
            setattr(Count, text, try_or_null(text))

        Count.total = sum(wow)

        return Count

    @property
    def friend_demographics(self) -> Demographics:
        res = requests.get("https://api.line.me/v2/bot/insight/demographic",
                           headers=self._newHeader).json()
        if not res['available']:
            raise OutOfService(
                "\n\nFriend demographics information is not available!\n")

        class Demographics:
            pass

        to = {
            "genders": ['gender', 'percentage'],
            "ages": ["age", 'percentage'],
            "areas": ['area', 'percentage'],
            "appTypes": ['appType', 'percentage'],
            "subscriptionPeriods": ["subscriptionPeriod", "percentage"]
        }
        for i in to:

            class _:
                pass

            for key in range(len(to[i])):
                try:
                    setattr(_, to[i][key], res[i][to[i][key]])
                except:
                    pass

            setattr(Demographics, i, _)

        return Demographics

    def get_friend_demographics(self):
        return self.friend_demographics
