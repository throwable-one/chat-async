# coding=utf-8


__author__ = 'Link'

import asyncio
from chat_async import chat_module, network_driver, websocket_driver


# NetworkDriver with base port 1234, WebsocketDriver as baseport 2345
drivers = [(1234, network_driver.NetworkDriver), (2345, websocket_driver.WebsocketDriver)]

loop = asyncio.get_event_loop()
chat = chat_module.ChatAsync("0.0.0.0", loop, drivers)
assert isinstance(loop, asyncio.AbstractEventLoop)
loop.run_until_complete(chat.launch())
loop.run_forever()