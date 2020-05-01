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


main_labels = {
    "statistics": "Статистика",
    "news": "Новости",
    "save_yourself": "Как защититься",
    "digital_pass": "Цифровой пропуск",
    "stickers": "Коронастикеры",
    "let_me_help": "Помочь",
    "back": "Назад"
}

main_keyboard = {
    "buttons": [
        [get_button(label=main_labels["statistics"], color="default"),
         get_button(label=main_labels["news"], color="default")],
        [get_button(label=main_labels["save_yourself"], color="default"),
         get_button(label=main_labels["digital_pass"], color="default")],
        [get_button(label=main_labels["stickers"], color="default"),
         get_button(label=main_labels["let_me_help"], color="default")],
    ]
}

news_labels = {
    "Russia": "Россия",
    "Moscow": "Москва",
    "Planet": "Планета",
    "Europe": "Европа"
}

news_keyboard = {
    "buttons": [
        [get_button(label=news_labels["Russia"], color="primary"),
         get_button(label=news_labels["Moscow"], color="primary")],
        [get_button(label=news_labels["Planet"], color="primary"),
         get_button(label=news_labels["Europe"], color="primary")],
        [get_button(label=main_labels["back"], color="negative")],
    ]
}

keyboards = {
    "main": main_keyboard,
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


while True:
    for event in long_poll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.from_user and not event.from_me:
                if event.message == main_labels["statistics"]:
                    message = "Заразились 3.300.000 человек"
                    vk_session.method('messages.send',
                                      {'user_id': event.user_id,
                                       'message': message,
                                       'random_id': random.random(),
                                       "keyboard": keyboards["main"]})
                elif event.message == main_labels["news"]:
                    change_keyboard(event.user_id, keyboards["news"], message=main_labels["news"])
                elif event.message == main_labels["back"]:
                    change_keyboard(event.user_id, keyboards["main"], message=main_labels["back"])
                elif event.message == main_labels["save_yourself"]:
                    message = "Надевайте маску и сохраняйте социальную дистанцию"
                    vk_session.method('messages.send',
                                      {'user_id': event.user_id,
                                       'message': message,
                                       'random_id': random.random(),
                                       "keyboard": keyboards["main"]})
                else:
                    message = f'Здравствуй дорогой пользователь @id{event.user_id} !' \
                              f'Выбери кнопку'
                    vk_session.method('messages.send',
                                      {'user_id': event.user_id,
                                       'message': message,
                                       'random_id': random.random(),
                                       "keyboard": keyboards["main"]})
