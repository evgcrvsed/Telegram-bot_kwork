import asyncio
import os
import re
from aiogram import Bot, Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
from dotenv import load_dotenv
from .cards_add_admin_handler import confirm_add_credentials
from main import db

load_dotenv()

token: str = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token=token)
router = Router()

ADMIN_GROUP_ID = '-1002114400170'



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

    if str(message.chat.id) == ADMIN_GROUP_ID:

        # если сообщение содержит номер карты, то  вызывем метод для записи в бд
        if re.search(r'\b(?:\d[ -]*?){13,16}\b', message.text.lower().strip()):
            card_number = message.text.lower().strip().replace("-", " ")
            if sum(c.isdigit() for c in card_number) > 16:
                return await message.answer("Введены некоректные реквезиты карты.")
            return await confirm_add_credentials(message, card_number=card_number)

        return

    info_reply_to_admin = await message.answer("Ваш вопрос был переслан администраторам, ожидайте ответа.")

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='Удалить это сообщение', callback_data=f"delete_from_admin_message"))

    await bot.send_message(
        chat_id=ADMIN_GROUP_ID,
        text=f"Отправитель: @{message.from_user.username}\n\n```Сообщение\n{message.text}```",
        parse_mode="MarkdownV2",
        reply_markup=builder.as_markup()
    )

    await asyncio.sleep(10)

    await info_reply_to_admin.delete()


@router.callback_query(F.data == "delete_from_admin_message")
async def delete_from_admin_message(clb: CallbackQuery):
    await clb.message.delete()