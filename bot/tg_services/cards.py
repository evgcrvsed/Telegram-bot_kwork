from random import choice

from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from main import db

router = Router()


async def give_credentials(clb, payment_type, prefix):
    select_option_message = clb.message

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='Вернуться к картам', callback_data=f"start"))

    text = ""
    if payment_type == "russian_cards":
        card_number = db.get_russian_credentials()
        if card_number:
            text = f'{prefix}: {choice(card_number)[1]}'
        else:
            text = "В данный момент карт данного типа не имеется."

    elif payment_type == "foreign_cards":
        card_number = db.get_foreign_credentials()
        if card_number:
            text = f'{prefix}: {choice(card_number)[1]}'
        else:
            text = "В данный момент карт данного типа не имеется."

    elif payment_type == "umoney":
        card_number = db.get_umoney_credentials()
        if card_number:
            text = f'{prefix}: {choice(card_number)[1]}'
        else:
            text = "В данный момент карт данного типа не имеется."

    elif payment_type == "crypto":
        card_number = db.get_crypto_credentials()
        if card_number:
            text = f'{prefix}: {choice(card_number)[1]}'
        else:
            text = "В данный момент карт данного типа не имеется."

    await clb.message.answer(text=text, reply_markup=builder.as_markup())

    await select_option_message.delete()


#
# async def give_credentials(clb, payment_type):
#     select_option_message = clb.message
#
#     builder = InlineKeyboardBuilder()
#     builder.row(InlineKeyboardButton(text='Вернуться к картам', callback_data=f"start"))
#
#     with open(f"bot/data/{filename}.txt", "r") as file:
#         numbers = [line.strip() for line in file]
#
#     await clb.message.answer(text=f'{prefix}: {choice(numbers)}', reply_markup=builder.as_markup())
#
#     await select_option_message.delete()


@router.callback_query(F.data == 'russian_cards')
async def russian_cards(clb: CallbackQuery):
    await give_credentials(clb, payment_type='russian_cards', prefix='Карта РФ')


@router.callback_query(F.data == 'foreign_cards')
async def russian_cards(clb: CallbackQuery):
    await give_credentials(clb, payment_type='foreign_cards', prefix='Зарубежная карта')


@router.callback_query(F.data == 'umoney')
async def russian_cards(clb: CallbackQuery):
    await give_credentials(clb, payment_type='umoney', prefix='Юмани')


@router.callback_query(F.data == 'crypto')
async def russian_cards(clb: CallbackQuery):
    await give_credentials(clb, payment_type='crypto', prefix='Крипто-кошелёк')


@router.callback_query(F.data == 'user_message')
async def user_message(clb: CallbackQuery):

    select_option_message = clb.message

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='Назад', callback_data=f"start"))

    text = "Отправьте сообщение в чат и оно дойдёт до администратора!"

    await clb.message.answer(text=text, reply_markup=builder.as_markup())

    await select_option_message.delete()


