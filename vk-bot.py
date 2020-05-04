import random
import json

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

import config

vk_session = vk_api.VkApi(token=config.vk_token)
long_poll = VkLongPoll(vk_session)
data = json.load(open("data.json", encoding="utf-8"))

keyboard_labels = dict()
info_labels = dict()
info = dict()
for button in data["buttons"]:
    keyboard_labels[button["name"]] = button["label"]["ru"]
    for button_ in button["buttons"]:
        info_labels[button_["name"]] = button_["label"]["ru"]
        info[button_["name"]] = "\n".join(button_["answer"]["ru"])
keyboard_labels[data["back_name"]] = "back" # data["back_label"]["ru"]


def get_button(label, color, payload=""):
    return dict(action={
        "type": "text",
        "label": label,
        "payload": json.dumps(payload)
    }, color=color)


def create_keyboard(buttons, main=False):
    result = dict()
    result["buttons"] = list()
    columns = 2

    for button_number in range(len(buttons)):
        if button_number % columns == 0:
            result["buttons"].append(list())
        row = button_number // columns

        color = "primary"
        if buttons[button_number]["type"] == "keyboard":
            color = "default"
        result["buttons"][row].append(get_button(label=buttons[button_number]["label"]["ru"], color=color))

    if not main:
        result["buttons"].append(list())
        result["buttons"][-1].append(get_button(label=data["back_name"], color="negative"))

    return result


keyboards = dict()
keyboards["back"] = create_keyboard(data["buttons"], main=True)
for keyboard_button in data["buttons"]:
    keyboards[keyboard_button["name"]] = create_keyboard(keyboard_button["buttons"])

# json to correct utf-8 string
for key in keyboards:
    keyboards[key] = str(json.dumps(keyboards[key], ensure_ascii=False).encode('utf-8').decode('utf-8'))


def change_keyboard(user_id, keyboard_name, message="Выберите кнопку"):
    vk_session.method('messages.send',
                      {
                          'user_id': user_id,
                          'message': message,
                          'random_id': random.random(),
                          "keyboard": keyboards[keyboard_name]
                      }
                      )


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
                                            key,
                                            message="Выберите кнопку")
                            break
                elif event.message in info_labels.values():
                    for key in info_labels:
                        if event.message == info_labels[key]:
                            print_info(event.user_id,
                                       message=info[key])
                            break
                else:
                    default_answer(event.user_id)
