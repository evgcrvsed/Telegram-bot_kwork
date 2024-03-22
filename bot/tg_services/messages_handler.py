import os
from aiogram import Bot, Dispatcher, types, Router, F
from dotenv import load_dotenv

load_dotenv()


token: str = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token=token)

ADMIN_GROUP_ID = '-1002114400170'

router = Router()


@router.message(F.text)
async def forward_to_admins(message: types.Message):
    # Пересылаем сообщение пользователя в группу администраторов
    await bot.forward_message(ADMIN_GROUP_ID, from_chat_id=message.chat.id, message_id=message.message_id)
    await message.answer("Ваше сообщение было переслано администраторам.")


# Обработка всех входящих сообщений в группе администраторов
@router.message()
async def reply_to_user(message: types.Message):
    user_id = message.forward_from.id
    await bot.send_message(user_id, message.text)
