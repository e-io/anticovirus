import lordofbots
import config


def main():
    new_data = lordofbots.Data("data.json")
    # old_data = lordofbots.Data("old_data.json")

    first_bot = lordofbots.Bot(new_data, "default", "tg", config.tg_first_token)
    second_bot = lordofbots.Bot(new_data, "default", "vk", config.vk_first_token)

    lord = lordofbots.LordOfBots()
    lord.run_bots(first_bot, second_bot)


if __name__ == "__main__":
    main()
