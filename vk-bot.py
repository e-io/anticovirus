import random

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

import config

vk_session = vk_api.VkApi(token=config.vk_token)
longpoll = VkLongPoll(vk_session)

#session_api = vk_session.get_api()

while True:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:

            if event.from_user and not event.from_me:
                message = f'Здравствуй пользователь @id{event.user_id}'
                vk_session.method('messages.send',
                                  {'user_id': event.user_id,
                                   'message': message,
                                   'random_id': random.random()})

