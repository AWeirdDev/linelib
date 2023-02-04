from urllib.parse import quote
from .database import *
from . import (
  commands as commands,
  rule
)

class SocialPlugins:
  """
  The LINE Social Plugins. (extension)
  """
  @staticmethod
  def share(url: str) -> str:
    """
    Returns a LINE Share Link. This is useful when you want a custom button.
    """
    return "https://social-plugins.line.me/lineit/share?url=" + str(quote(url))


class _depends:
  def __bool__(self):
    return False

  def __repr__(self):
    return "It Depends."

  def __eq__(self):
    return False

  def __hash__(self):
    return 0

  def __getitem__(self, k):
    return k


Depends = _depends()