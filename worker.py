import bot
import config

if __name__ == "__main__":
    bot = bot.Bot("tg", config.tg_token, config.lang, "data.json")
