import os, asyncio, logging, sys
from aiogram import Dispatcher, Bot
from dotenv import load_dotenv
load_dotenv()

from tg_services import start, cards

token: str = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token=token)
dp = Dispatcher()


async def main() -> None:
    dp.include_routers(
        start.router,
        cards.router
    )
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt as ex:
        print("Error: ", ex)
