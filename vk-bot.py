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


keyboard = {
    "one_time": False,
    "buttons": [
        [
            get_button(label="Статистика", color="positive"),
            get_button(label="Новости", color="negative")
        ]
    ]
}

keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))

# keyboard.add_button('Статистика', color=VkColor.POSITIVE)
# keyboard.add_line()
# keyboard.add_location_button()

# keyboard.add_line()
# keyboard.add_button('Новости', color=VkColor.NEGATIVE)

#keyboard.add_vkapps_button(app_id=vk_session.app_id,
 #                          owner_id=32334223432,
 #                          label="Клава",
 #                          hash="send_keyboard")

while True:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:

            if event.from_user and not event.from_me:
                message = f'Здравствуй пользователь1 @id{event.user_id}'
                vk_session.method('messages.send',
                                  {'user_id': event.user_id,
                                   'message': message,
                                   'random_id': random.random(),
                                   "keyboard": keyboard})

                #vk_session.method("messages.send",
                 #                 {"user_id": event.user_id,
                 #                  "message": "Нажми на кнопку",
                 #                  "keyboard": keyboard})
