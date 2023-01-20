<div align="center">
  <img src="https://user-images.githubusercontent.com/90096971/213644783-f525dd20-af78-4181-b665-fd6506410bde.png" alt="LINELIB Banner" />

# LINELIB
**The All-in-One LINE Bot Integration Solution.**

[![Get Started →](https://img.shields.io/badge/Get_Started_→-2ea44f?style=for-the-badge&logo=line&logoColor=ffffff)](https://github.com/AWeirdScratcher/linelib)

</div>

<div>
  <img src="https://user-images.githubusercontent.com/90096971/213690282-662ec477-b826-4fa4-9184-abcd8f0230d8.png" align="left" width="600" />
  <div>
    
  ## Optimized Source Code.
  Cleaner source code is beneficial because it is easier to read, understand, and maintain. It's easier for you to add new features, fix bugs, and understand how the code works. Clean code is also more efficient, as it is optimized for performance and is less likely to contain errors or bugs. It is also more reusable, allowing you to use it in other projects without having to rewrite it.
    
  [![  - See Example →](https://img.shields.io/badge/_-See_Example_→-06c755?style=for-the-badge&logo=python&logoColor=ffffff)](#1-quick-example)
    
  </div>

</div>

<br /><br /><br />

## With Extensions.
With LINELIB, you can easily and efficiently integrate various LINE services into your projects and applications, all with just a few lines of code. LINELIB simplifies the process of working with LINE services, making it more accessible and streamlined for developers of all skill levels. Whether you're looking to add messaging functionality, connect with LINE's social media platform, or utilize other LINE services, LINELIB makes it simple to do so with minimal code requirements.


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
