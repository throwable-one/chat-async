# coding=utf-8
"""
Module that supports telnet access to chat.
Use NetworkDriver class.
"""
import asyncio

from concurrent.futures import CancelledError, TimeoutError

__author__ = 'Link'

import chat_async


class _TalkManager:
    """
    Cares about new lines and string encoding
    """
    _NEW_LINE = "\r\n"

    def __init__(self, input_stream, output_stream):
        """

        :type input_stream asyncio.StreamReader
        :type output_stream asyncio.StreamWriter
        """
        self.__input_stream = input_stream
        self.__output_stream = output_stream
        self.__last_read_message = None

    def say(self, message, skip_new_line=False):
        """
        Say something to chat

        :param message what to say
        :param skip_new_line do not add new line
        :type message str
        :type skip_new_line bool
        """
        self.__output_stream.write((message + (_TalkManager._NEW_LINE if not skip_new_line else "")).encode())

    @asyncio.coroutine
    def read(self):
        """
        Read message from user in async manner.
        Yield from it, and read .last_read_message.
        """
        self.__last_read_message = yield from self.__input_stream.readline()

    @property
    def last_read_message(self):
        """
        :rtype str
        :return: last message read from channel using read()
        """
        return str(self.__last_read_message.decode()).rstrip(_TalkManager._NEW_LINE) if self.__last_read_message else ""


class NetworkDriver(chat_async.Driver):
    """
    Driver to access chat via simple tcp connection (telnet)
    """

    @asyncio.coroutine
    def input_handle(self, input_stream, output_stream):
        manager = _TalkManager(input_stream, output_stream)
        manager.say('*' * 10)
        manager.say("Welcome to chat ({})".format(','.join(self._chat_api.nicks_in_chat)))
        manager.say('*' * 10)
        manager.say("Your name: ", skip_new_line=True)
        yield from manager.read()
        nick = manager.last_read_message
        manager.say("Welcome, {}".format(nick))
        self._chat_api.enter_chat(nick)
        while self._chat_api.connection_opened:
            try:
                manager.say(": ", skip_new_line=True)
                yield from manager.read()
                self._chat_api.say_to_chat(manager.last_read_message)
            except (CancelledError, TimeoutError):
                return

    def output_handle(self, input_stream, output_stream):
        manager = _TalkManager(input_stream, output_stream)
        chat_queue = self._chat_api.subscribe_to_chat()
        manager.say("=" * 10)
        manager.say("Chat board ({})".format(','.join(self._chat_api.nicks_in_chat)))
        manager.say("=" * 10)
        while self._chat_api.connection_opened:
            message = yield from chat_queue.get()
            manager.say(message)