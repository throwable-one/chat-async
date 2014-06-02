chat-async
==========
## What is that?
Python asyncio-based chat. Chat is based on asyncio module available in python 3.4.
Entry point is `chat_async.chat_module.ChatAsync` class.

Chat could be extended by drivers: driver for network access (via telnet) and web access (via websockets) are included.

Check ``chat_server.py`` for running example.
## Running chat 

* Install websocket support with ``pip install websockets``
* Change ``web_client.html`` to set your IP there
* Check ``chat_server.py`` for ports.
* Run ``chat_server.py``
* Run ``web_interface.py``
* `telnet _your_ip_ 1234` to enter chat
* `telnet _your_ip_ 1235` to look at room
* navigate to ``http://<YOUR_IP>:8080/web_client.html`` to enter chat on web


