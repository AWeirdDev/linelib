<div align="center">
  <img src="https://user-images.githubusercontent.com/90096971/213644783-f525dd20-af78-4181-b665-fd6506410bde.png" alt="LINELIB Banner" />

# LINELIB
**The All-in-One LINE Bot Integration Solution.**

[![Get Started →](https://img.shields.io/badge/Get_Started_→-2ea44f?style=for-the-badge&logo=line&logoColor=ffffff)](https://github.com/AWeirdScratcher/linelib)
  
### Installation
Use the following, or clone this repository.
  
<img alt="pip install -U linelib" src="https://user-images.githubusercontent.com/90096971/213696060-a9ef7a7e-217c-4863-9b4a-5b6acaad0c69.png" width="400" />

</div>

# 🔑 Features[.](https://www.youtube.com/watch?v=H5v3kku4y6Q)

<div>
  <img src="https://user-images.githubusercontent.com/90096971/213690282-662ec477-b826-4fa4-9184-abcd8f0230d8.png" alt="Code Example" align="left" width="600" />
  <div>
    
  ## ✨ Optimized Source Code.
  Cleaner source code is beneficial because it is easier to read, understand, and maintain. It's easier for you to add new features, fix bugs, and understand how the code works. Clean code is also more efficient, as it is optimized for performance and is less likely to contain errors or bugs. It is also more reusable, allowing you to use it in other projects without having to rewrite it.
    
  [![  - See Example →](https://img.shields.io/badge/_-See_Example_→-06c755?style=for-the-badge&logo=python&logoColor=ffffff)](#1-quick-example)
    
  </div>

</div>

<br /><br /><br />

<img src="https://user-images.githubusercontent.com/90096971/213693396-83c0c20a-a30a-4648-b546-05c7019f10a0.png" width="300" alt="LINE Notify Mockup" align="right" />

## 🧩 With Extensions.
With LINELIB, you can easily and efficiently integrate various LINE services into your projects and applications, all with just a few lines of code. LINELIB simplifies the process of working with LINE services, making it more accessible and streamlined for developers of all skill levels. Whether you're looking to add messaging functionality, connect with LINE's social media platform, or utilize other LINE services, LINELIB makes it simple to do so with minimal code requirements.

LINELIB currently supports these LINE services:
- LINE Messaging API
- LINE Notify
- LINE Social Plugins

[![  - LINE Notify Example →](https://img.shields.io/badge/_-LINE_Notify_Example→-06c755?style=for-the-badge&logo=python&logoColor=ffffff)](#2-line-notify-example)


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
