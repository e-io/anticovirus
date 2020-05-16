# telebot is from pytelegrambotapi library
import json

import telebot
import vk_api


class Button:
    label = None
    keywords = None
    text = None
    buttons = None

    def __init__(self, dict):
        label = dict["label"]
        keywords = dict["keywords"]
        if "text" in dict:
            text = dict["text"]
        if "buttons" in dict:
            buttons = list()
            for button_ in dict["buttons"]:
                button = Button(button_["label"],
                                button_["keywords"])
                buttons.add(button)


class Bot:
    """
    This is universal class for any chat-bots
    """
    tg = None
    vk = None

    lang = None
    # type_ = None
    root = None
    start = None

    def __init__(self, type__, token_, lang_, data_):
        """
        Constructor
        type: tg (telegram) or vk
        token: token
        data: name of json file with all data for bot
        """
        # type_ = type__
        if type__ == "tg":
            tg = telebot.TeleBot(token_)
        elif type_ == "vk":
            vk = vk_api.VkApi(token=token_)
            raise (Exception("vk bot is not supported now"))
        else:
            raise (Exception("this type of bot is not supported"))

        data = json.load(open(data_), encoding="utf-8")
        start = Button(data["start"])

    def start(self):
        if tg:
            @bot.message_handler(commands=['start'])
            def start(message):
                tg.send_message(
                    message.chat.id,
                    "\n".join(start.text[lang])
                )

            @bot.message_handler(content_types=["text"])
            def answer(message):
                for keywords in start.keywords["ru"]:
                    if keyword in message:
                        start(message)
                        break
