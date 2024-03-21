from random import choice

from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()


async def give_credentials(clb, filename, prefix):
    select_option_message = clb.message

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='Вернуться к картам', callback_data=f"start"))

    with open(f"data/{filename}.txt", "r") as file:
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


