# coding=utf-8
"""
Module with chat class implementation
"""
import asyncio
from enum import Enum

from chat_async import ChatApi, Driver
import functools


__author__ = 'Link'


class _Direction(Enum):
    input = 0
    output = 1


class _Creator:
    def __init__(self, driver_class, direction, room_queue, client_queues, loop=asyncio.get_event_loop()):
        """
        :type direction _Direction
        :type room_queue asyncio.Queue
        :type client_queues list of asyncio.Queue
        """
        self.driver_class = driver_class
        self.direction = direction
        self.from_room_queue = None

        self.room_queue = room_queue
        self.client_queues = client_queues
        self.loop = loop

    def __call__(self, *args, **kwargs):
        return _ChatApiImpl(self)


class _ChatApiImpl(ChatApi, asyncio.StreamReaderProtocol):
    def __init__(self, creator_info):
        """
        :type creator_info _Creator
        """
        asyncio.StreamReaderProtocol.__init__(self, asyncio.StreamReader(), self.__handle, creator_info.loop)
        self.__creator_info = creator_info
        self.__from_room_queue = None
        self.__nick = None
        self.__connection_opened = False

    def connection_made(self, transport):
        super().connection_made(transport)
        self.__connection_opened = True


    @property
    def connection_opened(self):
        return self.__connection_opened

    @asyncio.coroutine
    def __handle(self, stream_reader, stream_writer):
        driver = self.__creator_info.driver_class(self)
        assert isinstance(driver, Driver)
        yield from driver.input_handle(stream_reader,
                                       stream_writer) if self.__creator_info.direction == _Direction.input else \
            driver.output_handle(stream_reader, stream_writer)

    def say_to_chat(self, message):
        assert self.__nick, "Enter room first"
        self.__creator_info.room_queue.put_nowait("{}: {}".format(self.__nick, message))

    def subscribe_to_chat(self):
        assert not self.__from_room_queue, "Already subscribed"
        self.__from_room_queue = asyncio.Queue()
        self.__creator_info.client_queues.append(self.__from_room_queue)
        return self.__from_room_queue

    def enter_chat(self, nick):
        self.__nick = nick
        self.say_to_chat("Hello")

    def eof_received(self):
        super().eof_received()
        self.__close_connection()

    def connection_lost(self, exc):
        super().connection_lost(exc)
        self.__close_connection()


    def __close_connection(self):
        self.__connection_opened = False
        if self.__from_room_queue:
            self.__creator_info.client_queues.remove(self.__from_room_queue)
            self.__from_room_queue = None
        if self.__nick:
            self.say_to_chat("I lost connection")
            self.__nick = None




class ChatAsync:
    """
    Chat async class
    """


    def __init__(self, host, loop=asyncio.get_event_loop(), driver_classes_tuple=None):
        """

        :param host: host to bind to
        :type host str
        """
        self.__host = host
        self.__driver_classes_tuple = driver_classes_tuple
        self.__room_queue = asyncio.Queue()
        self.__client_queues = []
        assert isinstance(loop, asyncio.AbstractEventLoop)
        self.__loop = loop


    @asyncio.coroutine
    def launch(self):
        """
        Launches server to loop
        """
        for (port, driver_class) in self.__driver_classes_tuple:
            input_protocol = _Creator(driver_class, _Direction.input, self.__room_queue,
                                      self.__client_queues,
                                      self.__loop)
            yield from self.__loop.create_server(input_protocol, self.__host, port)

            output_protocol = _Creator(driver_class, _Direction.output, self.__room_queue,
                                       self.__client_queues,
                                       self.__loop)
            yield from self.__loop.create_server(output_protocol, self.__host, int(port) + 1)

        while True:
            message = yield from self.__room_queue.get()
            for client_queue in self.__client_queues:
                client_queue.put_nowait(message)





