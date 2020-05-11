# Anticovirus

### Introduction

The name was created as a play on the words antivirus, coronavirus and covid-19

the master version of this bot functions at vk.com/anticv

the develop version functions at a different address in a closed group. The reference to it is not given because of the lack of need.

### Goal

The purpose of this bot is to inform people about the covid-19. How to avoid it, statistics of cases, useful links, etc.
When creating a bot, it was considered important to make it less dry, more fun. More interesting features. Developer hopes, bot doesn't look like something with dry, soulless informant or some kind of graduate project.

### Structure

The bot consists of the following files:

```
├── data.json - this is where all the contents of the bot are located. Outside of this file, there is not a word in Russian, not a word about the coronavirus
├── vk-bot.py - here is the entire logic of the bot. The bot "eats" at the start of data.json and starts a loop that runs through the longpoll functions in the vk_api package
├── config.py - two-line file with t0kЕn and language
├── requirements.txt - necessary packages for the bot to function
├── requirements.py - file generator for requirements.txt . Does not contain anything supernatural, is not necessary
├── runtime.txt - which version of Python is used. In our case, python is 3.7.4
├── Procfile - "worker" (performer), which you start using the switch in heroku
├── __init__.py - must be in the project according to heroku requirements, but may be empty
├── .gitignore - you need to make sure that the venv folder from pycharm, which is large and not meaningful for storage, is not pushed to github
```

### Functionality

This bot consists of ~6 menus. In each menu there are 4-6 buttons. When the button is clicked, information is displayed:
- number of infected people (statistics)
- useful links, such as where to get an electronic pass
- stickers with coronavirus
- how to help in the fight against coronavirus
- and much more

_____________________________

## Антиковирус

### Введение

Название создано как игра слов антивирус, коронавирус и ковид-19

master-версия данного бота функционирует по адресу vk.com/anticv

develop-версия функционирует по другому адресу в закрытой группе. Ссылка на нее не дается из-за отсутствия надобности.

### Цель 

Цель этого бота - информирование людей о коронавирусе. Как от него можно предостеречься, статистика заболевших, полезные ссылки и др.
При создании бота считалось важным сделать его менее сухим, более веселым, чтобы у него были какие-то интересные особенности. Чтобы он не выглядел как сухой бездушный информатор или какой-то дипломный проект.

### Структура

Бот состоит из следующих файлов:

```
├── data.json - здесь находится все содержимое бота. Вне этого файла нет ни слова по-русски, ни слова о коронавирусе
├── vk-bot.py - здесь находится вся логика бота. Бот «кушает» на старте data.json и запускает цикл, работающий через функции longpoll в пакете vk_api
├── config.py - двухстрочный файл с т0keном и языком
├── requirements.txt - необходимые пакеты для функционирования бота
├── requirements.py - генератор файла requirements.txt . Не содержит ничего сверхестественного, не является необходимым
├── runtime.txt - какая версия питона используется. В нашем случае python-3.7.4
├── Procfile - «воркер» (исполнитель), которого запускаешь переключателем в heroku
├── __init__.py - должен быть в проекте согласно требованиям heroku, однако может быть пустым
├── .gitignore - нужен чтобы объемная и малоосмысленная для хранения папка venv из pycharm не заливалась на гитхаб
```

### Функционал

Данный бот состоит из ~6 меню. В каждом меню есть по 4-6 кнопок. При нажатии на кнопку выдается информация:
- количество зараженных (статистика)
- полезные ссылки, например, где оформить электронный пропуск
- стикеры с коронавирусом
- как помочь в борьбе с коронавирусом
- и многое другое

