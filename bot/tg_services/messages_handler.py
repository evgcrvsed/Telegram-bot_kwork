import os

from aiogram import Bot, Router, types, F
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardBuilder
from dotenv import load_dotenv

load_dotenv()

token: str = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token=token)
router = Router()

ADMIN_GROUP_ID = '-1002114400170'

customer_id: id = None

@router.message(F.text)
async def forward_to_admins(message: types.Message):
    global customer_id

    if str(message.chat.id) == ADMIN_GROUP_ID:
        return await reply_to_user_handler(message, message.text, customer_id)

    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Ответить', callback_data='reply_to_user'))
    builder.add(InlineKeyboardButton(text='Проигнорировать', callback_data='ignore_to_user'))

    # Forward user message to admin group
    await bot.send_message(
        chat_id=ADMIN_GROUP_ID,
        text=f"Пользователь отправил вам запрос:\n *_{message.text}_*",
        parse_mode="MarkdownV2",
        reply_markup=builder.as_markup()
    )

    await message.answer("Ваше вопрос был переслан администраторам, ожидайте ответа.")

    customer_id = message.from_user.id


@router.callback_query(F.data == 'reply_to_user')
async def reply_to_user(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Введите ваш ответ на запрос пользователя: ")


@router.callback_query(F.data == 'ignore_to_user')
async def ignore_to_user(callback_query: types.CallbackQuery):
    message = callback_query.message

    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Вернуться назад", callback_data='start'))

    await callback_query.message.answer("Администратор отклонил ваш запрос", reply_markup=builder.as_markup())
    await message.delete()


async def reply_to_user_handler(message: types.Message, text: str, user_id):
    await message.answer(text="Ваш ответ был переадресован пользователю")
    replied_answer = f"Администратор ответил на ваш вопрос:\n *_{text}_*"
    await bot.send_message(chat_id=user_id, text=replied_answer, parse_mode="MarkdownV2")
