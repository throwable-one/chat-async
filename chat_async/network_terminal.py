import asyncio

__author__ = 'Link'

import chat_async


class _TalkManager:
    _NEW_LINE = "\r\n"

    def __init__(self, input_stream, output_stream):
        """

        :type input_stream asyncio.StreamReader
        :type output_stream asyncio.StreamWriter
        """
        self._input_stream = input_stream
        self._output_stream = output_stream
        self._last_read_message = None

    def say(self, message, skip_new_line=False):
        """

        :type message str
        """
        self._output_stream.write((message + (_TalkManager._NEW_LINE if not skip_new_line else "")).encode())

    @asyncio.coroutine
    def read(self):
        self._last_read_message = yield from self._input_stream.readline()

    @property
    def last_read_message(self):
        return str(self._last_read_message.decode()).rstrip(_TalkManager._NEW_LINE) if self._last_read_message else ""


class NetworkTerminal(chat_async.Terminal):
    @staticmethod
    def base_port():
        return 1234

    @asyncio.coroutine
    def handle_input(self, input_stream, output_stream):
        """

        :type input_stream asyncio.StreamReader
        :type output_stream asyncio.StreamWriter
        """
        talk_manager = _TalkManager(input_stream, output_stream)
        talk_manager.say("*" * 10)
        talk_manager.say("Welcome!")
        talk_manager.say("*" * 10)
        talk_manager.say("Enter your name: ", skip_new_line=True)
        yield from talk_manager.read()
        nick = talk_manager.last_read_message
        talk_manager.say("Hi, {}".format(nick))
        talk_manager.say("Say something")
        while True:
            talk_manager.say("{} : ".format(nick), skip_new_line=True)
            yield from talk_manager.read()
            self.chat_interface.say_to_chat(nick, talk_manager.last_read_message)

    @asyncio.coroutine
    def handle_output(self, input_stream, output_stream):
        """

        :type input_stream asyncio.StreamReader
        :type output_stream asyncio.StreamWriter
        """
        talk_manager = _TalkManager(input_stream, output_stream)
        talk_manager.say("=" * 10)
        talk_manager.say("Chat board")
        talk_manager.say("=" * 10)
        input_queue = self.chat_interface.subscribe()
        while True:
            (nick, message) = yield from input_queue.get()
            talk_manager.say("{}: {}".format(nick, message))
