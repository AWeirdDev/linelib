> **This project is currently _work-in-progress_, so this repo will remain blank until it's done.** <br>[Learn More](https://github.com/AWeirdScratcher) OR [Check The Status](undefined)

<div align="center">
  <img src="https://user-images.githubusercontent.com/90096971/198866047-361e88b7-d824-4736-a008-5c364e03e819.png" alt="Linelib Horizontal Image" />

# :rocket: Launch your bot to the next level.
Ever want your LINE Bot's source code cleaner, smoother? LINELIB is your choice.

[✨ Get Started →](https://google.com)

[💡 Examples →](https://github.com/AWeirdScratcher/linelib/tree/main/examples)

</div>

# 🧹 Say No More To Unorganized Code.

LINELIB has one of the best tools like events and action handlers, which saves you a lot of time!

Let's say you have a postback action, but you DON'T want another `if` statement to handle all of the action postbacks at once...

> **JUST TRY OUT ACTION HANDLERS!**<br>— The Wise Man

```py
def someEvent(...):
  action = New.PostbackAction(...)

  # Check This Out!
  @action.handle()
  def handleIt(ctx):
    ctx.reply("Responding to actions has never been easier like this.")
```

## ...with ✨ DATA STORAGE ✨!
Data storage helps you to identify a user, or store a pre-built function to execute next.

> **Everything. You can store EVERYTHING.**<br>— Also The Wise Man

```py
def stuff():
  print("I like cheeseburger")

action = New.PostbackAction(..., remember="a user", and_do=stuff)

@action.handle()
def handleIt(ctx, remember, and_do):
  #               ^^^^^^^^^^^^^^^^^
  #                simple as that.
  ctx.reply("I remember you: " + remember)
  and_do()
```

# 🤖 All, automated.
LINELIB uses `flask` to open the magic portal of HTTP.

> [Replit](https://replit.com) is a good option for hosting bots.<br>— Also Also The Wise Man

#### ~~Configuring webservers,<br> Managing Data,<br> Understanding LINE API Responses,~~
## 💻 Just Concentrate on Coding.
Hosting webservers, managing data, understanding how LINE API works... Say no more! LINELIB does all of that — Just for you.

Just look how **clean** using LINELIB Client:

```py
client = linelib.Client("channel secret", "channel access token")
```

...that's it. That's all you need to code. 

What about Flask Servers? Handlers?<br>Long Story Short, **we did it all for you.**

# 🚀 The Journey Awaits.
Let's just get started.

```py
client.run(host="0.0.0.0", port=8080)
```
<sub>Launch your bot!</sub>
