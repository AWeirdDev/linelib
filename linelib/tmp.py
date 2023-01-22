"""
Temporary database. This functionality was named `database` in the earlier version.
"""

class Tmp:
  """
  Temporary Database / Storage.
  """
  handle_action = {
    # it's just a storage
    'text': {}, # :Empty
    'postback': {} # :Empty
  }
  action_storage = {} # :Empty
  self_handler = {} # :Empty