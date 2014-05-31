# coding=utf-8
import asyncio

__author__ = 'Link'
from chat_async import Terminal
from websockets import server


class WebsocketTerminal(Terminal):
    @staticmethod
    def base_port():
        return 2345

    @asyncio.coroutine
    def handle_input(self, input_stream, output_stream):
        yield from WebsocketTerminal._create_protocol(self._input_handler, input_stream, output_stream)

    @asyncio.coroutine
    def handle_output(self, input_stream, output_stream):
        yield from WebsocketTerminal._create_protocol(self._output_handler, input_stream, output_stream)

    @staticmethod
    @asyncio.coroutine
    def _create_protocol(handler, input_stream, output_stream):
        protocol = server.WebSocketServerProtocol(handler)
        protocol.client_connected(input_stream, output_stream)
        yield from protocol.handler()

    @asyncio.coroutine
    def _input_handler(self, protocol, base):
        input_queue = self.chat_interface.subscribe()
        while True:
            (nick, message) = yield from input_queue.get()
            yield from protocol.send("{}: {}".format(nick, message))


    @asyncio.coroutine
    def _output_handler(self, protocol, base):
        nick = yield from protocol.recv()
        while True:
            message = yield from protocol.recv()
            self.chat_interface.say_to_chat(nick, message)