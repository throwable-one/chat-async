# coding=utf-8
"""
AsyncIo-based chat
"""
import abc
import asyncio
import random


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
    def get_some_phrase(self):
        """
        Say something funny
        :rtype str
        :return some phrase
        """
        pass


class RandomRobot(AbstractRobot):
    """
    Simple robot that say some words you provide to it
    """


    def __init__(self, *list_of_phrazes):
        """
        :param list_of_phrazes phrases to say
        :type list_of_phrazes list of str
        """
        self.__list_of_words = list_of_phrazes

    @property
    def name(self):
        return "RobotTheRandom"

    def get_some_phrase(self):
        return random.choice(self.__list_of_words)


class ChatApi(metaclass=abc.ABCMeta):
    """
    Interface that is injected in each driver. Driver uses it to communicate with chat.
    """

    @abc.abstractproperty
    def connection_opened(self):
        """
        :return is connection to client still opened or not
        :rtype bool
        """

        pass

    @abc.abstractmethod
    def enter_chat(self, nick):
        """
        Called by driver when user enters chat
        :param nick user nick
        :type nick str
        """
        pass

    @abc.abstractproperty
    def nicks_in_chat(self):
        """
        :return list of people in chat
        :rtype list of str
        """
        pass

    @abc.abstractmethod
    def say_to_chat(self, message):
        """
        To be called by driver when user says something to chat
        :param message: what did user said
        :type message str
        """
        pass

    @abc.abstractmethod
    def subscribe_to_chat(self):
        """
        To be used by driver to subscribe to chat.
        When subscribed, driver should fetch data from returned queue in asyncio style (using yield from).
        Each message is tuple of (nick, message)
        :return queue of (nick, message) tuples to be fetched asynchronously.
        :rtype asyncio.Queue
        """
        pass


class Driver(metaclass=abc.ABCMeta):
    """
    Driver represents chat terminal.
    It has 2 channels: input (from user to chat) and output (from chat to user).
    Both has 2 streams.

    Driver should:
    * use self._chat_api to work with chat
    * handle input and output asynchronously

    When user connected (input_handle is called), driver should ask user for nick and call self._chat_api.enter_chat.
    When output is connected, driver should subscribe (self._chat_api.subscribe_to_chat), fetch messages and show them
    to user.
    """

    def __init__(self, chat_api):
        """

        :type chat_api ChatApi
        """
        self._chat_api = chat_api

    @asyncio.coroutine
    @abc.abstractmethod
    def input_handle(self, input_stream, output_stream):
        """
        From user to chat connection.

        :type input_stream asyncio.StreamReader
        :type output_stream asyncio.StreamWriter
        """
        pass

    @asyncio.coroutine
    @abc.abstractmethod
    def output_handle(self, input_stream, output_stream):
        """
        From chat to user connection.

        :type input_stream asyncio.StreamReader
        :type output_stream asyncio.StreamWriter
        """
        pass