import os
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from aiogram.utils.keyboard import InlineKeyboardBuilder
from main import db
router = Router()

token: str = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token=token)
ADMIN_GROUP_ID = '-1002114400170'


async def set_commands(message: Message):
    if str(message.chat.id) == ADMIN_GROUP_ID:
        commands = [
            BotCommand(command="/start", description="Начать"),
            BotCommand(command="/show_info", description="Показать информацию"),
            BotCommand(command="/edit_instruction", description="Изменить инструкцию"),
            BotCommand(command="/delete_credentials", description="Удалить все карты"),
        ]
        return await bot.set_my_commands(commands)
    commands = [
        BotCommand(command="/start", description="Начать"),
    ]
    return await bot.set_my_commands(commands=commands)


def get_instruction():
    data = db.get_info()

    if data['instruction']:
        instruction_text = "\n    ".join(card_number for _, card_number in data['instruction'])
    else:
        instruction_text = "Данные инструкции отсутствуют!"

    return instruction_text


@router.callback_query(F.data == 'start')
@router.message(Command("start"))
async def start(clb: Message | CallbackQuery) -> None:
    if type(clb) == Message:
        await clb.answer(text=get_instruction())

        await set_commands(clb)

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
        await clb.message.reply_to_message.delete()

        await clb.message.edit_text(
            text='Выберите способ оплаты',
            reply_markup=builder.as_markup(),
            )
        # При Message
    except Exception as ex:
        await clb.answer(
            text='Выберите способ оплаты',
            reply_markup=builder.as_markup()
        )
