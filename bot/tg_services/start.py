import os
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton, BotCommand
from aiogram.utils.keyboard import InlineKeyboardBuilder
from main import db
router = Router()

token: str = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token=token)
ADMIN_GROUP_ID = '-1002114400170'


def get_instruction():
    data = db.get_info()
    header_instruction_text = "Инструкция по оплате\n\n"

    if data['instruction']:
        instruction_text = "\n".join(card_number for _, card_number in data['instruction'])
    else:
        instruction_text = "Данные инструкции отсутствуют!"

    resulted_text = header_instruction_text + instruction_text

    return resulted_text


@router.callback_query(F.data == 'start_instruction')
async def start_instruction_callback(clb: CallbackQuery) -> None:
    previous_message = clb.message
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='Назад', callback_data=f"start"))

    await clb.message.answer(
        text=get_instruction(),
        reply_markup=builder.as_markup(),
    )

    await previous_message.delete()


@router.callback_query(F.data == 'start')
@router.message(Command("start"))
async def start(clb) -> None:
    previous_message = clb

    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text='Карта РФ', callback_data=f"russian_cards"))
    builder.add(InlineKeyboardButton(text='Зарубежная карта', callback_data='foreign_cards'))
    builder.row(InlineKeyboardButton(text='Юмани', callback_data='umoney'))
    builder.add(InlineKeyboardButton(text='Крипто кошелек', callback_data='crypto'))
    builder.row(InlineKeyboardButton(text='Инструкция по оплате', callback_data=f"start_instruction"))  # Обработчик для кнопки "Инструкция по оплате"
    builder.row(InlineKeyboardButton(text='Отправить вопрос администратору', callback_data=f"user_message"))

    if type(clb) is CallbackQuery:
        # При Callback
        message = clb.bot.edit_message_reply_markup
        await message(
            chat_id=clb.message.chat.id,
            message_id=clb.message.message_id,
            reply_markup=builder.as_markup()
        )
        await clb.message.edit_text(
            text='Выберите способ оплаты',
            reply_markup=builder.as_markup(),
            )
        # При Message
    elif type(clb) is Message:
        clb: Message = clb
        await clb.answer(
            text='Выберите способ оплаты',
            reply_markup=builder.as_markup()
        )
        await previous_message.delete()


