import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

import config

vk_session = vk_api.VkApi(token=config.vk_token)
longpoll = VkLongPoll(vk_session)

#session_api = vk_session.get_api()
