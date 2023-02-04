from __future__ import annotations

import asyncio  # pip install asyncio
import base64
import hashlib
import hmac
import logging
import random
import time
from inspect import iscoroutinefunction, isfunction
from typing import Any, Callable, Union

from flask import Flask, jsonify, request
from flask_cors import CORS  # pip install flask-cors
from termcolor import colored, cprint

from .construct import (
  EventObject, 
  getContext, 
  getTriggerType, 
  modifiable
)

from .exceptions import Async as AsyncError
from .exceptions import Invalid
from .tmp import Tmp

# const
prefix = colored('linelib v2', 'light_green')


class Client:
  """
  Represents a Client.
  """

  # public:
  FUNCTION_NAME_OR_LISTENER: str = "@see-func"
  _VALID_EVENTS = ("ready", "text", "postback", "sticker", "unsend", "follow", "unfollow", "join", "leave", "memberJoined", "memberLeft", "videoPlayComplete", "beacon", "accountLink", "image", "video", "audio", "file", "location")
  _EVENTS = {} # Promise

  def __init__(self,
               channel_secret: str,
               channel_access_token: str,
               *args,
               **options: Any):
    self.CS = channel_secret
    self.CAT = channel_access_token

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    self.loop = loop  # if it is required

    for e in self._VALID_EVENTS:
      self._EVENTS[e] = []  # waiting for append
      Tmp.handle_action[e] = {} # database

    self.app = Flask("linelib.Client")
    CORS(self.app)

    self.headers = {
      "Authorization": f"Bearer {self.CAT}",
      "Content-Type": "application/json"
    }  # for quick access, yeah

  def createEvent(self, name: str, obj: type):
    self._EVENTS[name].append(obj)

  def emitEvents(self, name: str, *args: Any, **kwargs: Any):

    async def goOver():
      cache = self._EVENTS[name]
      done = []
      for handler in cache:
        async def doTask():
          if not name in ('ready', ):
            if handler.type == 'postback':
              func = getattr(args[0], 'data', None)
              if func:
                await Tmp.self_handler[func](*args, **kwargs)
                del Tmp.self_handler[func]
          await handler.emit(*args, **kwargs)

          if not name in ('ready', ):
            # args[0] => the context
              
            if getattr(args[0], "TYPE", None) in ['postback', 'datetime', 'rich_menu_switch']:
              try:
                del Tmp.action_storage[args[0].data]
              except Exception as err:
                print(f"\n\n{prefix} - {colored('Unknown Exception ~ TMP_DATA_DELETE', 'red')}:\n{err}\n\n")


          return  # finished, ends the complete task! B)
        
        task = asyncio.create_task(doTask())
        await task

        done.append(task)  # task completed
      res = asyncio.gather(*done)
      return res  # initial response

    loop = self.loop
    task = loop.create_task(goOver())
    loop.run_until_complete(task)

  def event(self,
            listener: Union[str, Callable] = FUNCTION_NAME_OR_LISTENER,
            *options) -> EventObject:
    """
    Represents an event listener. See `Client._VALID_EVENTS` to see a list of valid events.
    """
    if isfunction(listener):
      raise DeprecationWarning(
        "Linelib2 events are now switched to `@client.event()`. Make sure to add the '()' in order to work."
      )

    def wrapper(func, *args, **kwargs):
      if not (iscoroutinefunction(func)):
        raise AsyncError(
          "Async Error",
          f"Function '{func.__name__}(...)' should be an async function.")

      funcName = (listener or func._name__).replace("on_", "")
      if (funcName == "@see-func"):
        funcName = func.__name__.replace("on_", "")

      if (listener in [None, "@see-func"
                       ]) and (not funcName in self._VALID_EVENTS):
        raise Invalid(
          "Invalid Event",
          f"The event name '{funcName}' is not valid.\nConsider checking your spelling, or use the 'print(Client._VALID_EVENTS)' to see all existing event names."
        )

      res = EventObject({
        "func": func,  # handler
        "type": funcName,
        "options": options
      })

      self.createEvent(funcName, res)  # adds event handlers
      # required
      return res

    # required
    return wrapper

  @modifiable(req=dict)  # skip
  def request_then(self, req):
    pass  # default

  @modifiable(ctx=type)
  def payload_then(self, ctx):
    pass  # default

  @modifiable(handler=type, _=Any)
  def emit_before(self, handler, *args, **kwargs):
    """
    Runs before the linelib emits the event handlers.
    """
    pass  # default

  def run(self, **options):
    """
    Runs the LINE bot.

    `**options` - Arguments & options. Note that you must use named options, such as `log_level=ERROR`, `host='0.0.0.0'`, etc.
    """

    @self.app.route("/", methods=['GET', 'POST'])
    def index():
      if request.method == 'GET':
        return "LINE Bot"

      signature = request.headers.get('X-Line-Signature')
      body = request.get_data(as_text=True)
      hash = hmac.new(self.CS.encode('utf-8'), body.encode('utf-8'),
                      hashlib.sha256).digest()
      valid = hmac.compare_digest(signature.encode("utf-8"),
                                  base64.b64encode(hash))
      if not valid:
        raise Invalid(
          "Invalid Signature",
          f"\n\nAn invalid request was received. INFO:\nUser-Agent: {request.headers.get('User-Agent')}\nSignature Received: {signature}\nBody:\n{body}"
        )

      req: dict = request.json

      self.request_then(req)

      # requested
      for payload in req['events']:
        print(payload)
        t = getTriggerType(payload)
        context: type = getContext(
          t,
          self,
          payload  # duplicate
        )  # update: NOT *getContext(...)
        self.payload_then(context)
        self.emitEvents(t, context)

      if req['events'] == []:  # empty array
        cprint("\n\n🎉 Surprise!", "light_green")
        cprint(
          "Congratulations on your success — your webhook URL has been verified by LINE.\n\n"
        )
        return jsonify({"status": "Okay"})

      return jsonify({"status": "OK", "message": "Request accepted (linelib)"})

    START = time.time()

    @self.app.before_first_request
    def before_first():
      OKAY = time.time()
      TAKEN = OKAY - START
      if options.get('show_logs') in [None, True]:
        facts = [
          "LINE API has a slow delivery.", "Congrats on your success!",
          "I like chocolate.", "The 'New' method is deprecated.",
          "Try out LINE Notify with linelib!",
          "It's easy to view stats of your bot."
        ]
        print(
          f"\n\n{prefix} - App Running!\n{' ' * len('linelib v2 - ')}{random.choice(facts)}\n\n✨ {colored('ready', 'blue')} in {round(TAKEN * 1000)} ms\n\n"
        )

      self.emitEvents("ready")

    # launch application
    if options.get('show_logs') in [None, True]:
      print(
        f"\n\n{prefix} - Waiting for request...\n{' ' * len('linelib v2 - ')}Consider {colored('refreshing the webview.', 'red')}\n\n"
      )

    # option validation
    opt = options.copy()

    logging.getLogger('werkzeug').setLevel(logging.ERROR if (
      not "log_level" in options) else options.get('log_level'))

    if opt.get('log_level'):
      del opt['log_level']

    START = time.time()  # re-assign
    self.app.run(**opt, host="0.0.0.0", port=8080)

  def load_cog(self, cog: type):
    if not cog._ll_CONSTRUCTED:
      raise Invalid('Invalid Command Cog', f'We found out that your cog \'{cog.__name__}\' was not constrcted.\nPlease use `client.load_cog({cog.__name__}())` instead.')

    @self.event('text')
    async def on_mount(ctx):
        res = await cog.emit(ctx)
        if res == 'all-nf' and cog.show_not_found_log:
            print('\n' + colored('linelib v2', 'light_green') + " " + colored('COG', attrs=['bold', 'underline']) + f" - {cog.name}\n{' ' * len('linelib v2 ')}" + colored(f'Command \'{ctx.content.strip().split(" ")[0]}\' not found.', 'red') + '\n')

    return ...

  load_extension = load_cog

  # ================================

  async def sleep(self, seconds: int | float) -> None:
    """
    An asyncio method of `time.sleep`
    """
    await asyncio.sleep(seconds)


# hello if ur on github