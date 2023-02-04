<div align="center">
  <img src="https://user-images.githubusercontent.com/90096971/213644783-f525dd20-af78-4181-b665-fd6506410bde.png" alt="LINELIB Banner" />

# LINELIB v2.2
**The All-in-One LINE Bot Integration Solution.**

[![Get Started →](https://img.shields.io/badge/Get_Started_→-2ea44f?style=for-the-badge&logo=line&logoColor=ffffff)](https://github.com/AWeirdScratcher/linelib/wiki)


### Installation
Use the following, or clone this repository.
  
```ruby
$ pip install -U linelib
```

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

<img src="https://user-images.githubusercontent.com/90096971/213693396-83c0c20a-a30a-4648-b546-05c7019f10a0.png" width="150" alt="LINE Notify Mockup" align="right" />

## 🧩 With Extensions[.](https://i.kym-cdn.com/entries/icons/original/000/021/154/image.jpeg)
**With LINELIB, you can easily and efficiently integrate various LINE services into your projects and applications, all with just a few lines of code.** LINELIB simplifies the process of working with LINE services, making it more accessible and streamlined for developers of all skill levels. Whether you're looking to add messaging functionality, connect with LINE's social media platform, or utilize other LINE services, LINELIB makes it simple to do so with minimal code requirements.

LINELIB currently supports these LINE services:
- LINE Messaging API
- LINE Notify
- LINE Social Plugins

[![  - LINE Notify Example →](https://img.shields.io/badge/_-LINE_Notify_Example→-06c755?style=for-the-badge&logo=python&logoColor=ffffff)](#2-line-notify-example)

## 💪 More advanced.
**Create text commands like a pro.** 

Linelib helps you to quickly and efficiently create text commands by organizing them inside cogs!

<img alt="Greeting Command Source Code" src="https://user-images.githubusercontent.com/90096971/216757621-b3b462f9-c744-42f1-bb7c-340c6b6ebf21.png" width="800" />

<div align="center">
  
  # Ready to give it a shot?
  Oh my goodness, you're here! I'm hyped to see that you're willing to give it a go.
  
  Anyways, here are some helpful links that can get you around with LINELIB:
  
   [🚀 See More Examples](https://github.com/AWeirdScratcher/linelib)

   [📖 Documentation](https://github.com/AWeirdScratcher/linelib/wiki/documentation)
  
</div>

# 🎉 Examples.
"Don't just talk. Show me some examples!" I hear you say...

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

client = Client('channel secret', 'channel access token')
notify = Notify("access token")

@client.event('ready')
async def ready():
  await notify.notify("Daily News:\nLinelib version 2 has released!!11!")
  
client.run()
```

## 3: Simple Command Cog
This is a simple cog with the command "hello", which requires one argument (times) in order to work.

User: `hello 10`

Bot: `You greeted me 10 times!`

```py
from linelib import Client
from linelib.ext import commands

client = Client('channel secret', 'channel access token')

class MyCog(commands.Cog):
  @commands.cog_command(name="hello")
  async def greet_command(self, ctx, times: int):
    # "self" is required!
    await ctx.reply(f"You greeted me {times} times!")

client.load_cog(MyCog())
client.run()
```

## 4: Advanced Command Cog
This is a more advanced command cog with command rules, and rule rejection handlers.

The command (say) requires one argument "text", but you should add a "*" in the `greet_command` coroutine function to tell linelib to pass the rest of the message content into the argument ("text").

User: `say I love chocolate!`

Bot: `I love chocolate!`

1 second later...

User: `say I still love it.`

Bot: `The cooldown is 10 seconds long! Please wait.`

```py
from linelib import Client
from linelib.ext import commands, rule

client = Client('channel secret', 'channel access token')

class MyCog(commands.Cog):
  @commands.cog_command(
    name="say",
    rule=rule.CommandRule(
      rule="cooldown",
      seconds=10
    )
  )
  async def greet_command(self, ctx, *, text):
    # "self" is required!
    await ctx.reply(text)
    
  @greet_command.rule_reject
  async def rejected(self, ctx):
    await ctx.reply('The cooldown is 10 seconds long! Please wait.')

client.load_cog(MyCog())
client.run()
```

## 5: Custom Rule (Advanced)
Custom rules must have a function named "handler". The handler must return a valid boolean (`True` or `False`).

`True` represents that the user is able to use the command, vice versa.
```py
from linelib.ext import rule

class MyRule(rule.CommandRule):
  def handler(self, ctx):
    # ... your awesome code
    return True # must return True or False
    
MyRule(rule="based.custom") # Now, it's a valid command rule.
```
