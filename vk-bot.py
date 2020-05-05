import random
import json

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

import config

# starting loads
vk_session = vk_api.VkApi(token=config.vk_token)
long_poll = VkLongPoll(vk_session)
data = json.load(open("data.json", encoding="utf-8"))
lang = config.lang

# creating labels and info dictionaries
keyboard_labels = dict()
info_labels = dict()
info = dict()
for button in data["buttons"]:
    keyboard_labels[button["name"]] = button["label"][lang]
    for button_ in button["buttons"]:
        info_labels[button_["name"]] = button_["label"][lang]
        info[button_["name"]] = "\n".join(button_["answer"][lang])
keyboard_labels[data["back_name"]] = data["back_label"][lang]


# creating keyboards
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
        result["buttons"][row].append(get_button(label=buttons[button_number]["label"][lang], color=color))

    if not main:
        result["buttons"].append(list())
        result["buttons"][-1].append(get_button(label=data["back_label"][lang], color="negative"))

    return result


keyboards = dict()
keyboards[data["back_name"]] = create_keyboard(data["buttons"], main=True)
for keyboard_button in data["buttons"]:
    keyboards[keyboard_button["name"]] = create_keyboard(keyboard_button["buttons"])

# json to correct utf-8 string
for key in keyboards:
    keyboards[key] = str(json.dumps(keyboards[key], ensure_ascii=False).encode('utf-8').decode('utf-8'))


# management of runtime
def find_label_name(message, labels):
    message_ = message.lower()
    for name in labels:
        if message_ == labels[name].lower():
            return name

    return None


def change_keyboard(user_id, keyboard_name, message=data["choose_button"][lang]):
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
                       'message': data["not_recognized"][lang] +
                                  '. ' +
                                  data["choose_button"][lang],
                       'random_id': random.random(),
                       })


def message_handler():
    while True:
        for event in long_poll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.from_user and not event.from_me:
                    name = find_label_name(event.message, keyboard_labels)
                    if name:
                        change_keyboard(event.user_id,
                                        name,
                                        message=data["choose_button"][lang])
                        break
                    name = find_label_name(event.message, info_labels)
                    if name:
                        print_info(event.user_id,
                                   message=info[name])
                        break
                    default_answer(event.user_id)


if __name__ == '__main__':
    message_handler()
