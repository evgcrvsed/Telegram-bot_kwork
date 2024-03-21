import requests
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()


def get_instruction():
    with open('bot/data/instruction.txt', 'r', encoding='utf-8') as file:
        text = file.read()
    return text


@router.message(Command("start"))
async def start(msg: Message) -> None:
    await msg.answer(text=get_instruction())

    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text='Карта РФ', callback_data=f"russian_cards"))
    builder.add(InlineKeyboardButton(text='Зарубежная карта', callback_data='foreign_cards'))
    builder.row(InlineKeyboardButton(text='Юмани', callback_data='umoney'))
    builder.add(InlineKeyboardButton(text='Крипто кошелек', callback_data='crypto'))
    builder.row(InlineKeyboardButton(text='Инструкция по оплате', callback_data='instruction'))

    await msg.answer(
        text='Какой способ оплаты выбираете?',
        reply_markup=builder.as_markup()
    )
