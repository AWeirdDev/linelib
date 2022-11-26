import logging

Logger = logging.getLogger("linelib")
Logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
Logger.addHandler(handler)
