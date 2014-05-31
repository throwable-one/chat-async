# coding=utf-8


__author__ = 'Link'

import asyncio
from chat_async import chat_module, network_terminal, websocket_terminal


chat = chat_module.ChatAsync("192.168.1.3", [network_terminal.NetworkTerminal, websocket_terminal.WebsocketTerminal])
loop = asyncio.get_event_loop()
assert isinstance(loop, asyncio.AbstractEventLoop)
loop.run_until_complete(chat.launch())
loop.run_forever()