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

class ChatInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def subscribe(self):
        """

        :rtype asyncio.Queue
        """
        pass

    @abc.abstractmethod
    def say_to_chat(self, nick, message):
        pass

class Terminal(metaclass=abc.ABCMeta):
    def __init__(self, chat_interface):
        """

        :type chat_interface ChatInterface
        """
        self.chat_interface = chat_interface

    @staticmethod
    @abc.abstractmethod
    def base_port():
        """

        :rtype int
        """
        pass

    @asyncio.coroutine
    @abc.abstractmethod
    def handle_input(self, input_stream, output_stream):
        """

        :type input_stream asyncio.StreamReader
        :type output_stream asyncio.StreamWriter
        """
        pass

    @asyncio.coroutine
    @abc.abstractmethod
    def handle_output(self, input_stream, output_stream):
        """

        :type input_stream asyncio.StreamReader
        :type output_stream asyncio.StreamWriter
        """
        pass