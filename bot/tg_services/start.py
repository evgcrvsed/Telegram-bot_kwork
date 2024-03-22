import requests
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()


def get_instruction():
    with open('bot/data/instruction.txt', 'r', encoding='utf-8') as file:
        text = file.read()
    return text


@router.callback_query(F.data == 'start')
@router.message(Command("start"))
async def start(clb: Message | CallbackQuery) -> None:
    if type(clb) == Message:
        await clb.answer(text=get_instruction())


    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text='Карта РФ', callback_data=f"russian_cards"))
    builder.add(InlineKeyboardButton(text='Зарубежная карта', callback_data='foreign_cards'))
    builder.row(InlineKeyboardButton(text='Юмани', callback_data='umoney'))
    builder.add(InlineKeyboardButton(text='Крипто кошелек', callback_data='crypto'))
    builder.row(InlineKeyboardButton(text='Инструкция по оплате', callback_data=f"start"))
    builder.row(InlineKeyboardButton(text='Отправить вопрос администратору', callback_data=f"user_message"))

    try:
        # При Callback
        message = clb.bot.edit_message_reply_markup
        await message(
            chat_id=clb.message.chat.id,
            message_id=clb.message.message_id,
            reply_markup=builder.as_markup()
        )
        await clb.message.edit_text(
            text='Выберите способ оплаты',
            reply_markup=builder.as_markup()
            )
        # При Message
    except Exception as ex:
        await clb.answer(
            text='Выберите способ оплаты',
            reply_markup=builder.as_markup()
        )
