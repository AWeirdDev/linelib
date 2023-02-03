<details>
  <summary><h1>v2.2 coming out SOON!</h1></summary>
  <p>

Soon, we'll roll out the latest linelib update (`v2.2`) with bug fixes, and make your bots work more efficient. In addition, we're also putting back your favorite (probably) command cogs, but with better updates and features! Let's take a peek!

# 📢 New: Command Cogs!
With the latest update, commands and cogs will soon replace literally every single text handler! 

Let's see what we can do with them! 😈

## ⚙️ Simple Cog
The program below is a simple cog that greets you whenever you say `hello`:
```py
# version 2.2 (PREVIEW)
from linelib.ext import commands

class MyCog(commands.Cog):
  # cog_command MUST be in a cog:
  @commands.cog_command(name="hello")
  async def say_hello(self, ctx):
    await ctx.send("Hello, World!")
```

## 📦 ...with arguments & error handlers!
```py
# version 2.2 (PREVIEW)
from linelib import MissingArgument

# (inside a cog)
@commands.cog_command(name="drink")
async def drink(self, ctx, bottles: int):
  await ctx.send(f'You drank {bottles} of water!')

@drink.on_error
async def error_handler(self, ctx, error):
  if isinstance(error, MissingArgument): # missing a parameter ('bottles')
    await ctx.send('You missed some parameters!')
  else:
    raise error # if this error is something else...
```

## 🔑 Command not found? I got you covered!
```py
# version 2.2 (PREVIEW)

class MyCog(commands.Cog):
  ...
  
  async def not_found(self, ctx, command):
    print(f"Command {command} not found!")
```

# 📖 New: Command Rules!
Command rules help you to add rules to your commands which help you easily to detect if the users have the permission to use this command or not.

Even further, it is possible to modify it with ✨ command cooldowns! ✨

```py
# DECLARATION, DO NOT COPY
def __init__(self, *, rule: Literal["cooldown", "except", "for", "based.custom", "usage_limit"], **variations) -> None
```

## 🥶 Command Cooldowns & Rejects
```py
# version 2.2 (PREVIEW)
from linelib.ext import commands, rule

# (inside a cog)
@commands.cog_command(
  name="command",
  rule=rule.CommandRule(
    rule="cooldown",
    seconds=10
  )
)
async def my_command(self, ctx):
  await ctx.send('Hello!')
  
@my_command.rule_reject
async def rule_rejected(self, ctx):
  await ctx.send('You just greeted me!\nThe cooldown is 10 seconds long.')
```

# 😎 Load the Cog like a Pro
```py
client.load_cog(MyCog())
```

That's it! We also added some other features that are pretty stunning besides these! :)

[✨ Stay Tuned!](https://www.youtube.com/watch?v=h64PVy2h3qg)

***

  </p>
</details>

> Features coming soon: **Complete events**

<div align="center">
  <img src="https://user-images.githubusercontent.com/90096971/213644783-f525dd20-af78-4181-b665-fd6506410bde.png" alt="LINELIB Banner" />

# LINELIB (WIP)
**The All-in-One LINE Bot Integration Solution.**

[![Get Started →](https://img.shields.io/badge/Get_Started_→-2ea44f?style=for-the-badge&logo=line&logoColor=ffffff)](https://github.com/AWeirdScratcher/linelib)
  
### Installation
Use the following, or clone this repository.
  
<img alt="pip install -U linelib" src="https://user-images.githubusercontent.com/90096971/213696060-a9ef7a7e-217c-4863-9b4a-5b6acaad0c69.png" width="400" />

</div>

# 🔑 Features[.](https://google.com/search?q=dont+click+bro)

<div>
  <img src="https://user-images.githubusercontent.com/90096971/213690282-662ec477-b826-4fa4-9184-abcd8f0230d8.png" alt="Code Example" align="left" width="450" />
  <div>
    
  ## ✨ Optimized Source Code.
  Cleaner source code is beneficial because it is easier to read, understand, and maintain. It's easier for you to add new features, fix bugs, and understand how the code works. Clean code is also more efficient, as it is optimized for performance and is less likely to contain errors or bugs. It is also more reusable, allowing you to use it in other projects without having to rewrite it.
    
  [![  - See Example →](https://img.shields.io/badge/_-See_Example_→-06c755?style=for-the-badge&logo=python&logoColor=ffffff)](#1-quick-example)
    
  </div>

</div>

<br /><br /><br />

<img src="https://user-images.githubusercontent.com/90096971/213693396-83c0c20a-a30a-4648-b546-05c7019f10a0.png" width="300" alt="LINE Notify Mockup" align="right" />

## 🧩 With Extensions.
**With LINELIB, you can easily and efficiently integrate various LINE services into your projects and applications, all with just a few lines of code.** LINELIB simplifies the process of working with LINE services, making it more accessible and streamlined for developers of all skill levels. Whether you're looking to add messaging functionality, connect with LINE's social media platform, or utilize other LINE services, LINELIB makes it simple to do so with minimal code requirements.

LINELIB currently supports these LINE services:
- LINE Messaging API
- LINE Notify
- LINE Social Plugins

[![  - LINE Notify Example →](https://img.shields.io/badge/_-LINE_Notify_Example→-06c755?style=for-the-badge&logo=python&logoColor=ffffff)](#2-line-notify-example)

## 💪 Create Commands.
**Create text commands like a pro.** Linelib helps you to quickly and efficiently create text commands.

<div>
  <div align="left">

<img alt="Greeting Command Source Code" src="https://user-images.githubusercontent.com/90096971/213700257-0a2ef23c-1920-49df-9988-9e61a2491f71.png" width="600" />

</div>
  
<div align="right">


<img alt="Greeting Command Example" src="https://user-images.githubusercontent.com/90096971/213698679-4fd102db-dc4f-46f0-9059-b4e6f6da533c.png" />

</div>
</div>

<div align="center">
  
  # ( •̀ ω •́ )✧ Ready to give it a shot?
  Oh my goodness, you're here! I'm hyped to see that you're willing to give it a go.
  
  Anyways, here are some helpful links that can get you around with LINELIB.
  
   [🚀 See Examples](https://github.com/AWeirdScratcher/linelib)

   [🌍 Wiki](https://github.com/AWeirdScratcher/linelib/wiki)
  
</div>


# 🎉 Examples.
Here are some code examples (provided from the top).

## 1: Quick Example
```py
from linelib import Client

client = Client('channel secret', 'channel access token')

@client.event('ready')
async def ready():
  print('I am ready!')
  
client.run()
```

## 2: LINE Notify Example
```py
from linelib import Client
from linelib.notify import Notify

client = Client(...) # see "Quick Example"
notify = Notify("access token")

@client.event('ready')
async def ready():
  await notify.notify("Daily News:\nLinelib version 2 has released!!11!")
  
client.run()
```
