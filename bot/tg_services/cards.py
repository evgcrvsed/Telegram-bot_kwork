from random import choice

from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()


@router.callback_query(F.data=='russian_cards')
async def russian_cards(clb: CallbackQuery):
    select_option_message = clb.message

    with open("bot/data/russian_cards.txt", "r") as file:
        numbers = [line.strip() for line in file]

    await clb.message.answer(text=f'Карта РФ: {choice(numbers)}')
    await select_option_message.delete()


@router.callback_query(F.data=='foreign_cards')
async def russian_cards(clb: CallbackQuery):
    select_option_message = clb.message

    with open("bot/data/foreign_cards.txt", "r") as file:
        numbers = [line.strip() for line in file]

    await clb.message.answer(text=f'Зарубежная карта: {choice(numbers)}')


@router.callback_query(F.data=='umoney')
async def russian_cards(clb: CallbackQuery):
    select_option_message = clb.message

    with open("bot/data/umoney.txt", "r") as file:
        numbers = [line.strip() for line in file]

    await clb.message.answer(text=f'Юмани: {choice(numbers)}')
    await select_option_message.delete()


@router.callback_query(F.data=='crypto')
async def russian_cards(clb: CallbackQuery):
    select_option_message = clb.message

    with open("bot/data/crypto.txt", "r") as file:
        numbers = [line.strip() for line in file]

    await clb.message.answer(text=f'Крипто-кошелёк: {choice(numbers)}')
    await select_option_message.delete()
