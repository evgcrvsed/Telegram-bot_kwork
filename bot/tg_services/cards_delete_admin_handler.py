import os
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from aiogram.utils.keyboard import InlineKeyboardBuilder
from main import db
router = Router()


ADMIN_GROUP_ID = '-1002114400170'


@router.message(Command("delete_credentials"))
async def delete_credentials(msg: Message):
    if str(msg.chat.id) != ADMIN_GROUP_ID:
        return

    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text='Карта РФ', callback_data=f"delete_russian_cards"))
    builder.add(InlineKeyboardButton(text='Зарубежная карта', callback_data='delete_foreign_cards'))
    builder.row(InlineKeyboardButton(text='Юмани', callback_data='delete_umoney'))
    builder.add(InlineKeyboardButton(text='Крипто кошелек', callback_data='delete_crypto'))

    await msg.answer("Выберите какие типы карт вы хотите удалить.", reply_markup=builder.as_markup())


@router.callback_query(F.data == "delete_russian_cards")
async def delete_russian_cards(clb: CallbackQuery):
    db.delete_credentials(table_name="RussianCredentials")
    return await clb.message.answer(f"Все карты успешно удалены!")


@router.callback_query(F.data == "delete_foreign_cards")
async def delete_foreign_cards(clb: CallbackQuery):
    db.delete_credentials(table_name="ForeignCredentials")
    return await clb.message.answer(f"Все карты успешно удалены!")


@router.callback_query(F.data == "delete_umoney")
async def delete_umoney(clb: CallbackQuery):
    db.delete_credentials(table_name="UmoneyCredentials")
    return await clb.message.answer(f"Все карты успешно удалены!")


@router.callback_query(F.data == "delete_crypto")
async def delete_crypto(clb: CallbackQuery):
    db.delete_credentials(table_name="CryptoCredentials")
    return await clb.message.answer(f"Все карты успешно удалены!")
