import os, asyncio, logging
from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand
from dotenv import load_dotenv
from data.DataBase import DataBase
db = DataBase('data/database.db')
load_dotenv()

from tg_services import start, cards, messages_handler

token: str = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token=token)
dp = Dispatcher()


async def main() -> None:
    dp.include_routers(
        start.router,
        cards.router,
        messages_handler.router
    )
    await bot.delete_my_commands()

    await dp.start_polling(bot, skip_updates=True)




if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    db.create_table()
    try:
        asyncio.run(main())
    except KeyboardInterrupt as ex:
        print("Error: ", ex)
