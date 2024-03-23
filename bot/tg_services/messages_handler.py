import os
import re
from aiogram import Bot, Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message, InlineKeyboardButton
from aiogram.filters import Command
from dotenv import load_dotenv
from .cards_add_admin_handler import confirm_add_credentials
from main import db

load_dotenv()

token: str = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token=token)
router = Router()

ADMIN_GROUP_ID = '-1002114400170'

customer_requests = {}
info_reply_to_admin: types.Message = None


@router.message(Command("show_info"))
async def show_info(msg: Message):
    if str(msg.chat.id) != ADMIN_GROUP_ID:
        return

    data = db.get_info()

    if data['instruction']:
        instruction_text = "\n    ".join(card_number for _, card_number in data['instruction'])
    else:
        instruction_text = "Данные отсутствуют!"

    if data['russian_cards']:
        russian_cards_text = "\n    ".join(card_number for _, card_number in data['russian_cards'])
    else:
        russian_cards_text = "Данные отсутствуют!"

    if data['foreign_cards']:
        foreign_cards_text = "\n    ".join(card_number for _, card_number in data['foreign_cards'])
    else:
        foreign_cards_text = "Данные отсутствуют!"

    if data['umoney']:
        umoney_text = "\n    ".join(card_number for _, card_number in data['umoney'])
    else:
        umoney_text = "Данные отсутствуют!"

    if data['crypto']:
        crypto_text = "\n    ".join(card_number for _, card_number in data['crypto'])
    else:
        crypto_text = "Данные отсутствуют!"

    text = f"""
Instruction:
    {f'{instruction_text}'}
Russian cards:
    {f'{russian_cards_text}'}
Foreign cards:
    {f'{foreign_cards_text}'}
Umoney:
    {f'{umoney_text}'}
Crypto:
    {f'{crypto_text}'}
    """

    await msg.answer(text)


@router.message(Command("edit_instruction"))
async def edit_instruction(msg: Message):
    if str(msg.chat.id) != ADMIN_GROUP_ID:
        return

    instruction_text = (msg.text).replace('/edit_instruction ', '')

    db.edit_instruction(instruction_text)

    await msg.answer(f'Инструкция успешно изменена!')


@router.message(F.text)
async def forward_to_admins(message: types.Message):
    global info_reply_to_admin

    if str(message.chat.id) == ADMIN_GROUP_ID:

        # если сообщение содержит номер карты, то  вызывем метод для записи в бд
        if re.search(r'\b(?:\d[ -]*?){13,16}\b', message.text.lower().strip()):
            card_number = message.text.lower().strip().replace("-", " ")
            if sum(c.isdigit() for c in card_number) > 16:
                return await message.answer("Введены некоректные реквезиты карты.")
            return await confirm_add_credentials(message, card_number=card_number)

        # return await reply_to_user_handler(message, info_reply_to_admin)

    customer_requests[message.from_user.id] = message
    info_reply_to_admin = await message.answer("Ваш вопрос был переслан администраторам, ожидайте ответа.")

    # builder = InlineKeyboardBuilder()
    # builder.add(InlineKeyboardButton(text='Ответить', callback_data='reply_to_user'))
    #
    # await bot.forward_message(
    #     chat_id=ADMIN_GROUP_ID,
    #     from_chat_id=message.chat.id,
    #     message_id=message.message_id,
    # )
    # # Forward user message to admin group
    # await bot.send_message(
    #     chat_id=ADMIN_GROUP_ID,
    #     text=f"Пользователь отправил вам запрос:\n *_{message.text}_*",
    #     parse_mode="MarkdownV2",
    #     reply_markup=builder.as_markup()
    # )

    await bot.send_message(
        chat_id=ADMIN_GROUP_ID,
        text=f"Отправитель: @{message.from_user.username}\n\n```Сообщение\n{message.text}```",
        parse_mode="MarkdownV2"
    )



@router.message()
async def reply_to_user(message: types.Message):
    user_id = message.forward_from.id
    await bot.send_message(user_id, message.text)


#
# @router.callback_query(F.data == 'reply_to_user')
# async def reply_to_user(callback_query: types.CallbackQuery):
#     print(customer_requests.keys())
#     user_id = callback_query.from_user.id
#     if user_id not in customer_requests:
#         return
#     await callback_query.message.answer("Введите ваш ответ на запрос пользователя: ")


# async def reply_to_user_handler(message: types.Message, info_reply_admin):
#     print(customer_requests.keys())
#     user_id = message.from_user.id
#     if user_id not in customer_requests:
#         return
#
#     customer_message_data = customer_requests[user_id]
#     reply_admin_message = message.text
#
#     if customer_message_data is None:
#         return
#
#     await message.answer(text="Ваш ответ был переадресован пользователю")
#     builder = InlineKeyboardBuilder()
#     builder.row(InlineKeyboardButton(text='Вернуться к картам', callback_data=f"start"))
#
#     replied_answer = f"Администратор ответил на ваш вопрос:\n *_{reply_admin_message}_*"
#
#     await info_reply_admin.delete()
#
#     await bot.send_message(
#         chat_id=user_id,
#         reply_to_message_id=customer_message_data.message_id,
#         text=replied_answer, parse_mode="MarkdownV2",
#         reply_markup=builder.as_markup()
#     )

