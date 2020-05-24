import bot
import config


if __name__ == "__main__":
    bot = bot.Bot("tg", config.tg_token, "data.json", "ru")
    bot.add("vk", config.vk_token, "ru")
    bot.start_now()
