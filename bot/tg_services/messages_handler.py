import os

from aiogram import Bot, Router, types, F
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv

load_dotenv()

token: str = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token=token)
router = Router()

ADMIN_GROUP_ID = '-1002114400170'

customer_id: id = None
customer_request: id = None
info_reply_to_admin: types.Message = None


@router.message(F.text)
async def forward_to_admins(message: types.Message):
    global customer_id, customer_request, info_reply_to_admin

    if str(message.chat.id) == ADMIN_GROUP_ID:
        print(customer_request)
        return await reply_to_user_handler(message, customer_id, customer_request, info_reply_to_admin)
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Ответить', callback_data='reply_to_user'))

    # Forward user message to admin group
    await bot.send_message(
        chat_id=ADMIN_GROUP_ID,
        text=f"Пользователь отправил вам запрос:\n *_{message.text}_*",
        parse_mode="MarkdownV2",
        reply_markup=builder.as_markup()
    )

    info_reply_to_admin = await message.answer("Ваше вопрос был переслан администраторам, ожидайте ответа.")

    customer_request = message
    customer_id = message.from_user.id
    info_reply_to_admin = info_reply_to_admin


@router.callback_query(F.data == 'reply_to_user')
async def reply_to_user(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Введите ваш ответ на запрос пользователя: ")


async def reply_to_user_handler(message: types.Message, user_id, customer_message: types.Message, info_reply_admin_message):
    await message.answer(text="Ваш ответ был переадресован пользователю")
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='Вернуться к картам', callback_data=f"start"))

    replied_answer = f"Администратор ответил на ваш вопрос:\n *_{message.text}_*"

    await info_reply_admin_message.delete()

    await bot.send_message(
        chat_id=user_id,
        reply_to_message_id=customer_message.message_id,
        text=replied_answer, parse_mode="MarkdownV2",
        reply_markup=builder.as_markup()
    )
