import os
import re
from string import punctuation

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


async def reply_parse(replied_message: str) -> str:
    modified_text = ""
    for char in replied_message:
        if char in punctuation and char != "`":
            modified_text += "\\" + char
        else:
            modified_text += char

    return modified_text


@router.message(Command("show_info"))
async def show_info(msg: Message):
    if str(msg.chat.id) != ADMIN_GROUP_ID:
        return

    data = db.get_info()

    header_instruction_text = "Инструкция по оплате\n\n"
    if data['instruction']:
        instruction_body = "\n".join(card_number for _, card_number in data['instruction'])
    else:
        instruction_body = "Данные инструкции отсутствуют!"
    instruction_text = header_instruction_text + instruction_body + "\n\n"

    russian_cards_header = "РФ\n"
    if data['russian_cards']:
        russian_cards_body = "\n".join(card_number for _, card_number in data['russian_cards'])
    else:
        russian_cards_body = "Данные отсутствуют!"
    russian_cards_text = f"```{russian_cards_header + russian_cards_body}```\n\n"

    foreign_cards_header = "Зарубежные\n"
    if data['foreign_cards']:
        foreign_cards_body = "\n".join(card_number for _, card_number in data['foreign_cards'])
    else:
        foreign_cards_body = "Данные отсутствуют!"
    foreign_cards_text = f"```{foreign_cards_header + foreign_cards_body}```\n\n"

    umoney_header = "Юмани\n"
    if data['umoney']:
        umoney_body = "\n".join(card_number for _, card_number in data['umoney'])
    else:
        umoney_body = "Данные отсутствуют!"
    umoney_text = f"```{umoney_header + umoney_body}```\n\n"

    crypto_header = "Крипто\n"
    if data['crypto']:
        crypto_body = "\n".join(card_number for _, card_number in data['crypto'])
    else:
        crypto_body = "Данные отсутствуют!"
    crypto_text = f"```{crypto_header + crypto_body}```"

    resulted_text = instruction_text + \
        russian_cards_text + \
        foreign_cards_text + \
        umoney_text + \
        crypto_text

    parsed_text = await reply_parse(resulted_text)

    await msg.answer(parsed_text, parse_mode="MarkdownV2")


@router.message(Command("edit_instruction"))
async def edit_instruction(msg: Message):
    if str(msg.chat.id) != ADMIN_GROUP_ID:
        return

    await msg.answer(f'Напишите текст для инструкции (не менее 180 символов): ')


@router.message(F.text)
async def forward_to_admins(message: types.Message):
    if str(message.chat.id) == ADMIN_GROUP_ID:
        card_number = message.text.strip()
        # если сообщение содержит номер карты, то  вызывем метод для записи в бд
        if re.search(r'\b(?:\d[ -]*?){13,16}\b', card_number):
            card_number = card_number.replace("-", " ")
            if sum(c.isdigit() for c in card_number) > 16:
                return await message.answer("Введены некоректные реквезиты карты.")
            return await confirm_add_credentials(message, card_number=card_number)
        elif 26 <= len(card_number) <= 52 and card_number[0] in ['0', '1', '2', '3']:
            return await confirm_add_credentials(message, card_number=card_number)
        elif len(message.text) > 150:
            db.edit_instruction(message.text)
            return await message.answer(f'Инструкция успешно изменена!')
        return

    builder_customer = InlineKeyboardBuilder()
    builder_customer.row(InlineKeyboardButton(text='Назад', callback_data=f"start"))

    await message.answer(
        text="Ваш вопрос был переслан администраторам, ожидайте ответа.",
        reply_markup=builder_customer.as_markup()
    )

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='Удалить это сообщение', callback_data=f"delete_from_admin_message"))

    await bot.send_message(
        chat_id=ADMIN_GROUP_ID,
        text=f"Отправитель: @{message.from_user.username}\n\n```Сообщение\n{message.text}```",
        parse_mode="MarkdownV2",
        reply_markup=builder.as_markup()
    )


@router.callback_query(F.data == "delete_from_admin_message")
async def delete_from_admin_message(clb: CallbackQuery):
    await clb.message.delete()
