# telebot is from pytelegrambotapi library
import json
import asyncio
import random

import telebot
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


class Button:
    def __init__(self, dict):
        self.label = None
        self.keywords = None
        self.text = None
        self.buttons = None

        self.label = dict["label"]
        self.keywords = dict["keywords"]
        if "text" in dict:
            self.text = dict["text"]
        if "buttons" in dict:
            self.buttons = list()
            for button in dict["buttons"]:
                self.button = Button(button["label"],
                                     button["keywords"])
                self.buttons.add(button)


class Data:
    def __init__(self, file_):
        json_ = json.load(open(file), encoding="utf-8")

        self.langs = set()
        self.lang0 = json_["main_language"]
        self.langs.add(self.lang0)
        if "additional_languages" in json_:
            for lang in json_["additional_languages"]:
                self.langs.add(lang)

        self.start = Button(json_["start"])


class Bot:
    def __init__(self, data, lang, type_, token):
        self.data = data
        self.type = type_
        self.lang = lang

        self.api = api


class LordOfBots:
    """
    This is universal class for any chat-bots
    """
    def __init__(self):
        """
        Constructor
        """
        data = dict()
        bots = dict()


    def add_json(self, type_, token, data, lang=None):
        self.tg = None
        self.vk = None

        self.root = None

        self.lang = None


        self.add(type_, token, lang)

    def sender(self, source, id, text):
        if source == "tg":
            self.tg.send_message(
                id,
                text
            )
        elif source == "vk":
            self.vk.method('messages.send',
                           {
                               'user_id': id,
                               'message': text,
                               'random_id': random.random()
                           })

    def add(self, type_, token, lang):
        self.lang = lang

        if type_ == "tg":
            self.tg = telebot.TeleBot(token)
        elif type_ == "vk":
            self.vk = vk_api.VkApi(token=token)
        else:
            raise Exception("this type of bot is not being supported")

    def analyzer(self, source, id, message):
        message = message.lower()
        for keyword in self.start.keywords[self.lang]:
            if keyword in message:
                self.sender(source,
                            id,
                            "\n".join(self.start.text[self.lang]))
                return

    async def receiver_tg(self):
        @self.tg.message_handler(commands=['start'])
        def commands_start(message):
            self.sender(source,
                        id,
                        "\n".join(self.start.text[self.lang]))

        @self.tg.message_handler(content_types=["text"])
        def content_types_text(message):
            self.analyzer("tg", message.chat.id, message.text)

        await self.tg.polling(none_stop=True)

    async def receiver_vk(self):
        vk_longpoll = await VkLongPoll(self.vk)
        while True:
            for event in vk_longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW:
                    if event.from_user and not event.from_me:
                        await self.analyzer("vk", event.user_id, event.message)

    async def receiver(self):
        tasks = list()
        if self.vk: pass #tasks.append(asyncio.create_task(self.receiver_vk()))
        if self.tg: tasks.append(asyncio.create_task(self.receiver_tg()))
        await asyncio.gather(*tasks)

    def start_now(self):
        asyncio.run(self.receiver())
