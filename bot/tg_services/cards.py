from random import choice

from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.main import db

router = Router()

def get_cards(name):
    data = db.get_info()





async def give_credentials(clb, payment_type):
    select_option_message = clb.message

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='Вернуться к картам', callback_data=f"start"))

    with open(f"bot/data/{filename}.txt", "r") as file:
        numbers = [line.strip() for line in file]

    await clb.message.answer(text=f'{prefix}: {choice(numbers)}', reply_markup=builder.as_markup())

    await select_option_message.delete()


@router.callback_query(F.data == 'russian_cards')
async def russian_cards(clb: CallbackQuery):
    await give_credentials(clb, filename='russian_cards', prefix='Карта РФ')


@router.callback_query(F.data == 'foreign_cards')
async def russian_cards(clb: CallbackQuery):
    await give_credentials(clb, filename='foreign_cards', prefix='Зарубежная карта')


@router.callback_query(F.data == 'umoney')
async def russian_cards(clb: CallbackQuery):
    await give_credentials(clb, filename='umoney', prefix='Юмани')


@router.callback_query(F.data == 'crypto')
async def russian_cards(clb: CallbackQuery):
    await give_credentials(clb, filename='crypto', prefix='Крипто-кошелёк')


@router.callback_query(F.data == 'user_message')
async def user_message(clb: CallbackQuery):
    with open('bot/data/help.txt', 'r', encoding='utf-8') as file:
        text = file.read()

    select_option_message = clb.message

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='Назад', callback_data=f"start"))

    await clb.message.answer(text=text, reply_markup=builder.as_markup())

    await select_option_message.delete()
