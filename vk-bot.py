import random

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor as VkColor
import json
import config

vk_session = vk_api.VkApi(token=config.vk_token)
longpoll = VkLongPoll(vk_session)


# session_api = vk_session.get_api()

def get_button(label, color, payload=""):
    return dict(action={
        "type": "text",
        "payload": json.dumps(payload),
        "label": label
    }, color=color)


labels = {"statistics": "Статистика",
          "news": "Новости",
          "symptoms": "Симптомы",
          "save_yourself": "Как уберечься"
          }

keyboard = {
    "buttons": [
        [
            get_button(label=labels["statistics"], color="default"),
            get_button(label=labels["news"], color="primary")
        ],
        [get_button(label=labels["save_yourself"], color="positive")],
        [get_button(label=labels["symptoms"], color="negative")]
    ]
}

keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))

while True:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:

            if event.from_user and not event.from_me:

                if event.message == labels["statistics"]:
                    message = "Заразились 3.300.000 человек"
                    vk_session.method('messages.send',
                                      {'user_id': event.user_id,
                                       'message': message,
                                       'random_id': random.random(),
                                       "keyboard": keyboard})
                elif event.message == labels["news"]:
                    message = "Число зараженных в США перевалило за один миллион человек"
                    vk_session.method('messages.send',
                                      {'user_id': event.user_id,
                                       'message': message,
                                       'random_id': random.random(),
                                       "keyboard": keyboard})
                elif event.message == labels["save_yourself"]:
                    message = "Надевайте маску и сохраняйте социальную дистанцию"
                    vk_session.method('messages.send',
                                      {'user_id': event.user_id,
                                       'message': message,
                                       'random_id': random.random(),
                                       "keyboard": keyboard})
                elif event.message == labels["symptoms"]:
                    message = "Тяжело дышать. Головная боль"
                    vk_session.method('messages.send',
                                      {'user_id': event.user_id,
                                       'message': message,
                                       'random_id': random.random(),
                                       "keyboard": keyboard})
                else:
                    message = f'Здравствуй пользователь @id{event.user_id}'
                    vk_session.method('messages.send',
                                      {'user_id': event.user_id,
                                       'message': message,
                                       'random_id': random.random(),
                                       "keyboard": keyboard})
