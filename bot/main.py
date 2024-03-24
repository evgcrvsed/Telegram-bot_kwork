import os, asyncio, logging
import time
from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand, BotCommandScopeChat
from dotenv import load_dotenv
from data.DataBase import DataBase
db = DataBase('data/database.db')
load_dotenv()

from tg_services import start, cards, messages_handler, cards_delete_admin_handler, cards_add_admin_handler

token: str = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token=token)
dp = Dispatcher()
ADMIN_GROUP_ID = '-1002114400170'

async def main() -> None:
    dp.include_routers(
        start.router,
        cards.router,
        cards_delete_admin_handler.router,
        cards_add_admin_handler.router,
        messages_handler.router,
    )
    await bot.delete_my_commands()
    basic_commands = [
        BotCommand(command="/start", description="Начать/Меню")
    ]

    await bot.set_my_commands(commands=basic_commands)
    admin_commands = [
        BotCommand(command="/start", description="Начать"),
        BotCommand(command="/show_info", description="Показать информацию"),
        BotCommand(command="/edit_instruction", description="Изменить инструкцию"),
        BotCommand(command="/delete_credentials", description="Удалить все карты"),
        BotCommand(command='/add_credentials', description="Добавить новую карту")
    ]

    setted_comands = await bot.set_my_commands(commands=admin_commands, scope=BotCommandScopeChat(chat_id=ADMIN_GROUP_ID))
    print(setted_comands)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    db.create_table()
    while True:
        try:
            asyncio.run(main())
        except KeyboardInterrupt as ex:
            print("Error: ", ex)
        print('Бот перезапускается!')
        time.sleep(5)
