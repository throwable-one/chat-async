# coding=utf-8
"""
Module with chat class implementation
"""
import asyncio
from chat_async import Terminal, ChatInterface

__author__ = 'Link'


class _Handler:
    def __init__(self, terminal_class, chat):
        self._terminal_class = terminal_class
        self.chat = chat

    @asyncio.coroutine
    def handle_input(self, reader, writer):
        terminal = self._terminal_class(self.chat)
        assert isinstance(terminal, Terminal)
        yield from terminal.handle_input(reader, writer)

    @asyncio.coroutine
    def handle_output(self, reader, writer):
        terminal = self._terminal_class(self.chat)
        assert isinstance(terminal, Terminal)
        yield from terminal.handle_output(reader, writer)


class ChatAsync(ChatInterface):
    """
    Chat async class
    """

    def __init__(self, host, terminal_classes):
        """

        :param host: host to bind to
        :type host str
        """
        self._host = host
        self._terminal_classes = terminal_classes
        self._client_queues = []
        self._queue = asyncio.Queue()

    def subscribe(self):
        queue = asyncio.Queue()
        self._client_queues.append(queue)
        return queue

    def say_to_chat(self, nick, message):
        self._queue.put_nowait((nick, message))


    @asyncio.coroutine
    def launch(self):
        """
        Launches server to loop
        """
        for terminal_class in self._terminal_classes:
            client_queue = asyncio.Queue()
            self._client_queues.append(client_queue)
            # terminal = terminal_class(client_queue, self._queue)
            # assert isinstance(terminal, Terminal), "Terminal is not terminal!"
            base_port = int(terminal_class.base_port())
            yield from asyncio.start_server(_Handler(terminal_class, self).handle_input, self._host, base_port)
            yield from asyncio.start_server(_Handler(terminal_class, self).handle_output, self._host, base_port + 1)

        while True:
            message = yield from self._queue.get()
            for queue in self._client_queues:
                queue.put_nowait(message)





