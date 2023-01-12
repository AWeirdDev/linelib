

<div align="center">
  <img src="https://user-images.githubusercontent.com/90096971/198866047-361e88b7-d824-4736-a008-5c364e03e819.png" alt="Linelib" />

# :tada: Surprise!
We're announcing — **Linelib v2**! Code faster and get ready for a huge upgrade to your LINE bot! :sparkles:

(NOT RELEASED + FINISHED YET!)

</div>

## 💪 FASTER.
Linelib v2 will be using **async**. Hold up! It's not that hard as you think. Just add an `async` keyword!

```py
from linelib import Client

client = Client(...)

@client.event('ready')
async def rdy():
  print('Bro thinks he ready')

client.run()
```

### 🤔️ Why async?
In Linelib version 2, async reduces the system CPU usage by awaiting. This is a huge help when it comes to low-resource environment, and it also works faster on large requests!

## 📦 Knock, knock. It's your package!
No, not that kind of Python package. I meant databases.

Linelib v2 creates a temporary database which helps you to get previous data from previous requests if you're making a form-like chat.

> Note that you can create multiple event handlers with same event names in the update.
```py
@client.event('text')
async def handler1(ctx):
  if not ctx.stored_user:
    await ctx.store(
      "user", # the user's own data
      ctx.text # the data (message content)
    )
    await ctx.reply("I remember you now!")
  else:
    await ctx.reply("Your previous message:\n" + ctx.stored_user)
    await ctx.storage.clear() # say goodbye (reset)
```

## 😳 I'm watching you.
Linelib v2 contains the `wait_for` feature, which is a big help to you if you want your bot to wait for the user's reply.

```py
# inside a listener
@client.wait_for('text')
async def then(e):
  print('Execute me first!')

await then.wait()
await ctx.reply('...then execute me!')

... # other code
```

## 🧹 Time to a tidy up.
🤬🤬😤 bro i hate messy code!1!!111

Use the command method to create commands — instead of overloading your poor, poor text event listener.

```py
@client.command(name="/yo")
async def yo(ctx):
  await ctx.reply("ayo mr white")
```

### 🙈 ...with lots of-
**Options.** Linelib allows you to fully customize your code with options. Such as `QueuedSending` (event tool), `sleepThen` (async outside), and more...

(🤩 Yes, they are built in!)

## 🐛 GO AWAY, BUGS!
Here are some bug fixes (currently):

- Handle multiple events from LINE API
- Slow event emitting
- Unused codes that's taking over your RAM
- Long names & code-tip not showing up

...and more, as I release it.

<div align="center">

# Stay Tuned!
Updates are coming soon!

Really, soon... 😈

<sub>(So I can see people suffer from changing every single function to async)</sub>

</div>
