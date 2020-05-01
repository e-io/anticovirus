import random
import json

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor as VkColor

import config

vk_session = vk_api.VkApi(token=config.vk_token)
long_poll = VkLongPoll(vk_session)


def get_button(label, color, payload=""):
    return dict(action={
        "type": "text",
        "label": label,
        "payload": json.dumps(payload)
    }, color=color)


keyboard_labels = {
    "statistics": "Статистика",
    "news": "Новости",
    "save_yourself": "Как защититься",
    "digital_pass": "Цифровой пропуск",
    "stickers": "Коронастикеры",
    "let_me_help": "Помочь",
    # "back" means main keyboard
    "back": "Назад"
}

main_keyboard = {
    "buttons": [
        [get_button(label=keyboard_labels["statistics"], color="default"),
         get_button(label=keyboard_labels["news"], color="default")],
        [get_button(label=keyboard_labels["save_yourself"], color="default"),
         get_button(label=keyboard_labels["digital_pass"], color="default")],
        [get_button(label=keyboard_labels["stickers"], color="default"),
         get_button(label=keyboard_labels["let_me_help"], color="default")],
    ]
}

info_labels = {
    # news
    "Russia": "Россия",
    "Moscow": "Москва",
    "Planet": "Планета",
    "Europe": "Европа",
    # statistics
    "on Russia": " по России",
    "on Moscow": " по Москве",
    "on Planet": " по Планете",
    "on Europe": " по Европе"
}

news_keyboard = {
    "buttons": [
        [get_button(label=info_labels["Russia"], color="primary"),
         get_button(label=info_labels["Moscow"], color="primary")],
        [get_button(label=info_labels["Planet"], color="primary"),
         get_button(label=info_labels["Europe"], color="primary")],
        [get_button(label=keyboard_labels["back"], color="negative")],
    ]
}

statistics_keyboard = {
    "buttons": [
        [get_button(label=info_labels["Russia"], color="primary"),
         get_button(label=info_labels["Moscow"], color="primary")],
        [get_button(label=info_labels["Planet"], color="primary"),
         get_button(label=info_labels["Europe"], color="primary")],
        [get_button(label=keyboard_labels["back"], color="negative")],
    ]
}

keyboards = {
    "back": main_keyboard,
    "news": news_keyboard
}


def change_keyboard(keyboard):
    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))

    return keyboard


# main_keyboard = change_keyboard(main_keyboard)
for key in keyboards:
    keyboards[key] = change_keyboard(keyboards[key])

del main_keyboard
del news_keyboard


# main_keyboard = json.dumps(main_keyboard, ensure_ascii=False).encode('utf-8')
# main_keyboard = str(main_keyboard.decode('utf-8'))


# for key in keyboards:
#    keyboards[key] = json.dumps(keyboards[key], ensure_ascii=False).encode('utf-8')
#    keyboards[key] = str(keyboards[key].decode('utf-8'))


def change_keyboard(user_id, keyboard, message="Выберите кнопку"):
    vk_session.method('messages.send',
                      {'user_id': user_id,
                       'message': message,
                       'random_id': random.random(),
                       "keyboard": keyboard})


def print_info(user_id, message):
    vk_session.method('messages.send',
                      {'user_id': user_id,
                       'message': message,
                       'random_id': random.random(),
                       })


def default_answer(user_id):
    vk_session.method('messages.send',
                      {'user_id': user_id,
                       'message': "Ваша команда не распознана. Выберите кнопку.",
                       'random_id': random.random(),
                       })


while True:
    for event in long_poll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.from_user and not event.from_me:
                if event.message in keyboard_labels.values():
                    for key in keyboard_labels:
                        if event.message == keyboard_labels[key]:
                            change_keyboard(event.user_id,
                                            keyboards[key],
                                            message=keyboard_labels[key])
                            break
                elif event.message in info_labels.values():
                    for key in info_labels:
                        if event.message == info_labels[key]:
                            print_info(event.user_id,
                                       message="pass")
                            break
                else:
                    default_answer(event.user_id)
