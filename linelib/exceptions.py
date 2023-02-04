# throw

class Base(Exception):
  def __init__(self, title, txt):
    txt = f"\n\n[{title}]\n" + txt
    super().__init__(txt) # end
 
class Async(Base):
  """
  Async related exceptions. (mainly)
  """
  pass

class Invalid(Base):
  """
  Anything that's invalid.
  """
  pass

class Usage(Base):
  """
  Usage exceptions.
  """
  pass

class ClientException(Exception):
  """
  A client-based exception. (Things that are related to the Client.)
  """
  pass

class MissingArgument(Exception):
    """
    Represents a command argument was not passed into.
    """
    pass