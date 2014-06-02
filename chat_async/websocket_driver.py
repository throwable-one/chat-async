# coding=utf-8
"""
Module that supports websocket access to chat.
Use WebsocketDriver class.
"""
import asyncio

__author__ = 'Link'
from chat_async import Driver
from websockets import server


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
        while self._chat_api.connection_opened:
            message = yield from room_queue.get()
            yield from protocol.send(message)

    @asyncio.coroutine
    def __input_loop(self, protocol, base):
        """

        :type protocol server.WebSocketServerProtocol
        :param base:
        :return:
        """
        nick = yield from protocol.recv()
        self._chat_api.enter_chat(nick)
        while self._chat_api.connection_opened:
            message = yield from protocol.recv()
            self._chat_api.say_to_chat(message)



