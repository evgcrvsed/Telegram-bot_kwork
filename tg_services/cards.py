from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()

@router.callback_query(F.data=='russian_cards')
async def russian_cards(clb: CallbackQuery):
    await clb.message.answer(text='russian_cards_data')
    # await clb.message.edit_reply_markup()
