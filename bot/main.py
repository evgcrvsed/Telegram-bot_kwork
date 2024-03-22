import os, asyncio, logging
from aiogram import Dispatcher, Bot
from dotenv import load_dotenv
from bot.data.DataBase import DataBase
load_dotenv()

from tg_services import start, cards, messages_handler

token: str = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token=token)
dp = Dispatcher()
db = DataBase('bot/data/Instruction.db')

async def main() -> None:
    dp.include_routers(
        start.router,
        cards.router,
        messages_handler.router
    )
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    db.create_table()

    try:
        asyncio.run(main())
    except KeyboardInterrupt as ex:
        print("Error: ", ex)
