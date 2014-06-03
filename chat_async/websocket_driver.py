# coding=utf-8
"""
Module that supports websocket access to chat.
Use WebsocketDriver class.

TODO: Get rid of second channel.

Check js/websocket_client for example client.

JS client protocol: Each message consists of 2 parts: "message" and "text". See "Protocol" section below.
"""
import asyncio

__author__ = 'Link'
from chat_async import Driver
from websockets import server
from json.encoder import JSONEncoder

# Protocol


_GET_NICK = 'get_nick'  # Client should send nick with next message
_ADD = 'add'  # Client should add nick to list of "people in chat" (data in "text" field)
_REMOVE = 'remove'  # should remove it
_TEXT = 'text'  # Should display text (data in "text" field)


class WebsocketDriver(Driver):
    """
    Supports websocket access to chat.
    Client needs to open 2 connections (input on baseport and output on baseport+1).
    First, client needs to send a nick. After that, messages could be sent.
    """

    def input_handle(self, input_stream, output_stream):
        yield from self.__create_protocol(self.__input_loop, input_stream, output_stream)

    def output_handle(self, input_stream, output_stream):
        yield from self.__create_protocol(self.__output_loop, input_stream, output_stream)


    @asyncio.coroutine
    def __create_protocol(self, handler, reader, writer):
        protocol = server.WebSocketServerProtocol(handler)
        protocol.client_connected(reader, writer)
        yield from protocol.handler()

    @asyncio.coroutine
    def __output_loop(self, protocol, base):
        """

        :type protocol server.WebSocketServerProtocol
        :param base:
        :return:
        """
        room_queue = self._chat_api.subscribe_to_chat()
        json_encoder = JSONEncoder()
        current_people = self._chat_api.nicks_in_chat
        while self._chat_api.connection_opened:
            message = yield from room_queue.get()
            yield from protocol.send(json_encoder.encode({"message": _TEXT, "text": message}))
            if current_people != self._chat_api.nicks_in_chat:
                current_people = self._chat_api.nicks_in_chat
                yield from protocol.send(
                    json_encoder.encode({"message": _ADD, "text": ",".join(self._chat_api.nicks_in_chat)}))

    @asyncio.coroutine
    def __input_loop(self, protocol, base):
        """

        :type protocol server.WebSocketServerProtocol
        :param base:
        :return:
        """
        json_encoder = JSONEncoder()
        yield from protocol.send(json_encoder.encode({"message": _GET_NICK}))
        nick = yield from protocol.recv()
        self._chat_api.enter_chat(nick)
        yield from protocol.send(
            json_encoder.encode({"message": _ADD, "text": ",".join(self._chat_api.nicks_in_chat)}))
        while self._chat_api.connection_opened:
            message = yield from protocol.recv()
            self._chat_api.say_to_chat(message)



