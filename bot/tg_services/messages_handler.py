import os

from aiogram import Bot, Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message, InlineKeyboardButton
from aiogram.filters import Command
from dotenv import load_dotenv

from main import db

load_dotenv()

token: str = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token=token)
router = Router()

ADMIN_GROUP_ID = '-1002114400170'

customer_id: id = None
customer_request: id = None
info_reply_to_admin: types.Message = None


@router.message(Command("show_info"))
async def show_info(msg: Message):
    if str(msg.chat.id) != ADMIN_GROUP_ID:
        return

    data = db.get_info()

    if data['instruction']:
        instruction_text = "\n    ".join(card_number for _, card_number in data['instruction'])
    else:
        instruction_text = "Данные отсутствуют!"

    if data['russian_cards']:
        russian_cards_text = "\n    ".join(card_number for _, card_number in data['russian_cards'])
    else:
        russian_cards_text = "Данные отсутствуют!"

    if data['foreign_cards']:
        foreign_cards_text = "\n    ".join(card_number for _, card_number in data['foreign_cards'])
    else:
        foreign_cards_text = "Данные отсутствуют!"

    if data['umoney']:
        umoney_text = "\n    ".join(card_number for _, card_number in data['umoney'])
    else:
        umoney_text = "Данные отсутствуют!"

    if data['crypto']:
        crypto_text = "\n    ".join(card_number for _, card_number in data['crypto'])
    else:
        crypto_text = "Данные отсутствуют!"

    text = f"""
Instruction:
    {f'{instruction_text}'}
Russian cards:
    {f'{russian_cards_text}'}
Foreign cards:
    {f'{foreign_cards_text}'}
Umoney:
    {f'{umoney_text}'}
Crypto:
    {f'{crypto_text}'}
    """

    await msg.answer(text)


@router.message(Command("edit_instruction"))
async def edit_instruction(msg: Message):
    if str(msg.chat.id) != ADMIN_GROUP_ID:
        return

    instruction_text = (msg.text).replace('/edit_instruction ', '')

    db.edit_instruction(instruction_text)

    await msg.answer(f'Инструкция успешно изменена!')


@router.message(Command("add_credentials"))
async def add_credentials(msg: Message):
    if str(msg.chat.id) != ADMIN_GROUP_ID:
        return

    data = (msg.text).replace('/add_credentials ', '').rstrip().split()

    table_name = data[0]
    card_number = " ".join(data[1:])

    if 'rus' in table_name.lower():
        result = db.add_credentials(table_name="RussianCredentials", card_number=card_number) # rus
    elif 'um' in table_name.lower():
        result = db.add_credentials(table_name="UmoneyCredentials", card_number=card_number) # umoney
    elif 'for' in table_name.lower():
        result = db.add_credentials(table_name="ForeignCredentials", card_number=card_number) # foreign
    elif 'cry' in table_name.lower():
        result = db.add_credentials(table_name="CryptoCredentials", card_number=card_number) # crypto
    else:
        await msg.answer("Повторите запрос! (неправильно ввели вид кошелька)\nДоступны: russian, umoney, foreign, crypto")
        return
    if result == 1:
        await msg.answer(f"Номер карты {card_number} уже существует!!")
        return
    await msg.answer(f"Номер карты {card_number} успешно добавлен!")


@router.message(Command("delete_credentials"))
async def delete_credentials(msg: Message):
    if str(msg.chat.id) != ADMIN_GROUP_ID:
        return

    table_name = (msg.text).replace('/delete_credentials ', '')

    if 'rus' in table_name.lower():
        result = db.delete_credentials(table_name="RussianCredentials")  # rus
    elif 'um' in table_name.lower():
        result = db.delete_credentials(table_name="UmoneyCredentials")  # umoney
    elif 'for' in table_name.lower():
        result = db.delete_credentials(table_name="ForeignCredentials")  # foreign
    elif 'cry' in table_name.lower():
        result = db.delete_credentials(table_name="CryptoCredentials")  # crypto
    else:
        await msg.answer(
            "Повторите запрос! (неправильно ввели вид кошелька)\nДоступны: russian, umoney, foreign, crypto")

    await msg.answer(f"Все карты типа {table_name} успешно очищены!")


@router.message(F.text)
async def forward_to_admins(message: types.Message):
    global customer_id, customer_request, info_reply_to_admin

    if str(message.chat.id) == ADMIN_GROUP_ID:
        return await reply_to_user_handler(message, customer_id, customer_request, info_reply_to_admin)

    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Ответить', callback_data='reply_to_user'))

    # Forward user message to admin group
    await bot.send_message(
        chat_id=ADMIN_GROUP_ID,
        text=f"Пользователь отправил вам запрос:\n *_{message.text}_*",
        parse_mode="MarkdownV2",
        reply_markup=builder.as_markup()
    )

    info_reply_to_admin = await message.answer("Ваше вопрос был переслан администраторам, ожидайте ответа.")

    customer_request = message
    customer_id = message.from_user.id
    info_reply_to_admin = info_reply_to_admin


@router.callback_query(F.data == 'reply_to_user')
async def reply_to_user(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Введите ваш ответ на запрос пользователя: ")


async def reply_to_user_handler(message: types.Message, user_id, customer_message: types.Message, info_reply_admin_message):

    if user_id is None:
        return

    await message.answer(text="Ваш ответ был переадресован пользователю")
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='Вернуться к картам', callback_data=f"start"))

    replied_answer = f"Администратор ответил на ваш вопрос:\n *_{message.text}_*"

    await info_reply_admin_message.delete()

    await bot.send_message(
        chat_id=user_id,
        reply_to_message_id=customer_message.message_id,
        text=replied_answer, parse_mode="MarkdownV2",
        reply_markup=builder.as_markup()
    )

