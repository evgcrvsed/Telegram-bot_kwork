from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()
ADMIN_GROUP_ID = '-1002114400170'

from bot.main import db


@router.message(Command("add_credentials"))
async def add_credentials(msg: Message):
    if str(msg.chat.id) != ADMIN_GROUP_ID:
        return

    return await msg.answer("Введите номер карты/кошелька")


@router.message(Command("add_credentials"))
async def confirm_add_credentials(message: Message, card_number: str):
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text='Карта РФ', callback_data=f"add_russian_cards:{card_number}"))
    builder.add(InlineKeyboardButton(text='Зарубежная карта', callback_data=f'add_foreign_cards:{card_number}'))
    builder.row(InlineKeyboardButton(text='Юмани', callback_data=f'add_umoney:{card_number}'))
    builder.add(InlineKeyboardButton(text='Крипто кошелек', callback_data=f'add_crypto:{card_number}'))

    await message.answer(
        f"Выберите к какой группе относится реквезиты карты: {card_number}",
        reply_markup=builder.as_markup()
    )


@router.callback_query(F.data.startswith("add_russian_cards"))
async def add_russian_cards(clb: CallbackQuery):
    card_number = clb.data.split(":")[1]
    result = db.add_credentials(table_name="RussianCredentials", card_number=card_number)
    if result == 1:
        return await clb.message.answer(f"Номер карты {card_number} уже существует!!")
    await clb.message.answer(f"Номер карты {card_number} успешно добавлен!")


@router.callback_query(F.data.startswith("add_foreign_cards"))
async def add_foreign_cards(clb: CallbackQuery):
    card_number = clb.data.split(":")[1]
    result = db.add_credentials(table_name="ForeignCredentials", card_number=card_number)
    if result == 1:
        return await clb.message.answer(f"Номер карты {card_number} уже существует!!")
    await clb.message.answer(f"Номер карты {card_number} успешно добавлен!")


@router.callback_query(F.data.startswith("add_umoney"))
async def add_umoney(clb: CallbackQuery):
    card_number = clb.data.split(":")[1]
    result = db.add_credentials(table_name="UmoneyCredentials", card_number=card_number)
    if result == 1:
        return await clb.message.answer(f"Номер карты {card_number} уже существует!!")
    await clb.message.answer(f"Номер карты {card_number} успешно добавлен!")


@router.callback_query(F.data.startswith("add_crypto"))
async def add_crypto(clb: CallbackQuery):
    card_number = clb.data.split(":")[1]
    result = db.add_credentials(table_name="CryptoCredentials", card_number=card_number)
    if result == 1:
        return await clb.message.answer(f"Номер крипто-кошелька {card_number} уже существует!!")
    await clb.message.answer(f"Номер карты {card_number} успешно добавлен!")
