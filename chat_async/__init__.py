# coding=utf-8
"""
AsyncIo-based chat
"""
import abc
import asyncio


__author__ = 'Link'


class AbstractRobot(metaclass=abc.ABCMeta):
    """
    Interface each robot implements
    """

    @abc.abstractproperty
    def name(self):
        """

        :return: Robot name
        """
        pass

    @asyncio.coroutine
    @abc.abstractmethod
    def say_something(self, output_stream):
        """
        Say something funny
        :param output_stream: stream where to say something
        :type output_stream asyncio.streams.StreamWriter
        """
        pass

class ChatApi(metaclass=abc.ABCMeta):

    @abc.abstractproperty
    def connection_opened(self):
        """

        :rtype bool
        """

        pass

    @abc.abstractmethod
    def enter_chat(self, nick):
        """

        """
        pass

    @abc.abstractmethod
    def say_to_chat(self, message):
        pass

    @abc.abstractmethod
    def subscribe_to_chat(self):
        """

        :rtype asyncio.Queue
        """
        pass


class Driver(metaclass=abc.ABCMeta):
    def __init__(self, chat_api):
        """

        :type chat_api ChatApi
        """
        self._chat_api = chat_api

    @asyncio.coroutine
    @abc.abstractmethod
    def input_handle(self, input_stream, output_stream):
        """

        :type input_stream asyncio.StreamReader
        :type output_stream asyncio.StreamWriter
        """
        pass

    @asyncio.coroutine
    @abc.abstractmethod
    def output_handle(self, input_stream, output_stream):
        """

        :type input_stream asyncio.StreamReader
        :type output_stream asyncio.StreamWriter
        """
        pass