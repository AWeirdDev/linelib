from __future__ import annotations

class Storage:
  pass

class DatabaseTable:
  """
  A database that helps you to store specific information. You could do this with keys.

  **Example**
  ```py
  # run_me.py
  from linelib.ext import DatabaseTable
  
  DatabaseTable.remember = "I've remembered this!"
  ```
  ```py
  # main.py
  import run_me # runs 'run_me.py'
  from linelib.ext import DatabaseTable

  print(DatabaseTable.remember) # I've remembered this!
  ```
  """
  pass
