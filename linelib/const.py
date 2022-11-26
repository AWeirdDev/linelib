# this is not javascript

class DEFAULT:
    api = "https://api.line.me/v2/bot"

    class portal:
        host = "0.0.0.0"
        port = 8080
    
    class STATIC:
        UDS_HTML = """<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>linelib</title>
            <style>
                body { transition: all 1s cubic-bezier(.55,0,.1,1); }
            </style>
            <script type="text/javascript">
                window.addEventListener("DOMContentLoaded", (e /* ignored */)=>{
                        document.querySelector("#pr-btn").onmouseover = function () {
                        document.body.style.backgroundColor = "#282828";
                    }
                        document.querySelector("#pr-btn").onmouseout = function () {
                        document.body.style.backgroundColor = "#121212";
                    }
                    document.getElementById("host").textContent = window.location.host;
                })
                
            </script>
        </head>
        <body style="font-family: sans-serif; background-color: #121212; color: white;">
            <main style="display: flex; flex-direction: column; align-items: center; min-height: 100%; margin-top: 50px;">
                <h3 style="color: #07b53b; font-weight: bold; font-weight: 800; cursor: pointer;">LINE<span style="color: white; font-weight: 800; text-transform: uppercase;">LIB</span></h3>
                <h1 style="font-size: 3rem;">Hi Mom</h1>
                <p style="color: #aaaaaa">HOST:</p>
                <p id='host'></p><br><br>
                <p style="color: #aaaaaa;">This is a test server for <code style="background: #323232; display: inline-block; border-radius: 4px; margin: 2px;">linelib</code>. Trust me, it's going to be a FUN ride!<br><br>
                Get started by reading the docs, or simply change <code style="background: #323232; display: inline-block; border-radius: 4px; margin: 2px;">UseDevServer()</code> to your own flask app!</p>
                <button id="pr-btn" style="margin-top: 25px; background: #07b53b; padding: 16px 32px; border: none; border-radius: 6px; font-size: 15px; cursor: pointer; color: white;">
                    <a href="https://youtube.com/watch?v=dQw4w9WgXcQ" target="_blank" style="text-decoration: none; color: white;">LINE Button Example</a>
                </button>
            </main>
        </body>
        </html>
        """
