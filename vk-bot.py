import random
import json

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor as VkColor

import config

vk_session = vk_api.VkApi(token=config.vk_token)
long_poll = VkLongPoll(vk_session)

data = json.load(open("data.json", encoding="utf-8"))

keyboard_labels = {
    "statistics": "Статистика",
    "news": "Новости",
    "save_yourself": "Как защититься",
    "digital_pass": "Цифровой пропуск",
    "stickers": "Коронастикеры",
    "let_me_help": "Помочь",
    # "back" means main keyboard
    "back": "back"
}

info_labels = {
    # news
    "Russia": "Россия",
    "Moscow": "Москва",
    "Planet": "Планета",
    "USA": "США",
    # statistics
    "on Russia": "по России",
    "on Moscow": "по Москве",
    "on Planet": "по Планете",
    "on USA": "по США"
}

info = {
    "Russia": "Россия догоняет Италию. Как развивается эпидемия у нас и в других странах — изучаем на графиках\n"
              "https://yandex.ru/news/story/Rossiya_dogonyaet_Italiyu"
              "._Kak_razvivaetsya_ehpidemiya_u_nas_i_v_drugikh_stranakh__izuchaem_na_grafikakh"
              "--66ecdf32e8655ae8c5d8acf6ac5e0527?lr=66&lang=ru&persistent_id=96187916&rubric=koronavirus&from=rubric",
    "Moscow": "1. В Москве разъяснили правила получения пропуска для поездки на дачу \n" \
              "https://yandex.ru/news/story/V_Moskve_razyasnili_pravila_polucheniya_propuska_dlya_poezdki_na_dachu"
              "--0e0e22c6649bdfd799d0964ee8906aa0?lr=66&lang=ru&stid=qW5rCuXgGhVoZ2r_zZph&persistent_id=96094307"
              "&rubric=koronavirus&from=rubric"
              "\n\n2. В Подмосковье вводят обязательное ношение масок \n"
              "https://yandex.ru/news/story/V_Podmoskove_vvodyat_obyazatelnoe_noshenie_zashhitnykh_masok_na_ulice"
              "--bd6244c13cfb453067267d6406fd54dc?lr=66&lang=ru&stid=ALLlx30HKLqUaxqaua6b&persistent_id=96112641"
              "&rubric=koronavirus&from=rubric",
    "USA": "Трамп заявил о лабораторном происхождении нового коронавируса\n"
           "https://yandex.ru/news/story/Tramp_zayavil_o_laboratornom_proiskhozhdenii_novogo_koronavirusa"
           "--e0eb1333fade8697500a04fef35d3fde?lr=66&lang=ru&stid=iVLnQgMrVGzkORws9Xgt&persistent_id=96157169&rubric"
           "=koronavirus&from=rubric",
    "Planet": "Обнаружено новое средство от коронавируса\n"
              "https://yandex.ru/news/story/Obnaruzheno_novoe_sredstvo_ot_koronavirusa"
              "--a03cc51a96448e72d906a0cacd8f6ee3?lr=66&lang=ru&stid=wzGnRgkOM6WbCi5oIDkS&persistent_id=96078312"
              "&rubric=koronavirus&from=rubric",
    "on Russia": "Заразились за сегодня 7000 человек",
    "on Moscow": "Заразились за сегодня 3500 человек",
    "on USA": "Заразились за сегодня 31300 человек",
    "on Planet": "Заразились за сегодня 70000 человек",
}


def get_button(label, color, payload=""):
    return dict(action={
        "type": "text",
        "label": label,
        "payload": json.dumps(payload)
    }, color=color)


def create_keyboard(buttons, main=False):
    result = dict()
    result["buttons"] = list()
    columns = 3

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


def json_to_string(keyboard):
    return str(json.dumps(keyboard, ensure_ascii=False).encode('utf-8').decode('utf-8'))


for key in keyboards:
    keyboards[key] = json_to_string(keyboards[key])


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
