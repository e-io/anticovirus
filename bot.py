# telebot is from pytelegrambotapi library
import json

import telebot
import vk_api


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


class Bot:
    """
    This is universal class for any chat-bots
    """
    def __init__(self, type, token, lang, data):
        """
        Constructor
        type: tg (telegram) or vk
        token: token
        data: name of json file with all data for bot
        """
        self.tg = None
        self.vk = None

        self.lang = None
        self.start = None
        self.root = None

        self.lang = lang
        self.data = json.load(open(data), encoding="utf-8")
        self.start = Button(self.data["start"])

        if type == "tg":
            self.tg = telebot.TeleBot(token)
        elif type == "vk":
            self.vk = vk_api.VkApi(token=token)
            raise (Exception("vk bot is not supported now"))
        else:
            raise (Exception("this type of bot is not supported"))

    def start_now(self):
        if self.tg:
            @self.tg.message_handler(commands=['start'])
            def start_answer(message):
                self.tg.send_message(
                    message.chat.id,
                    "\n".join(self.start.text[self.lang])
                )

            @self.tg.message_handler(content_types=["text"])
            def answer(message):
                for keyword in self.start.keywords[self.lang]:
                    if keyword in message.text:
                        start_answer(message)
                        break

            self.tg.polling(none_stop=True)
