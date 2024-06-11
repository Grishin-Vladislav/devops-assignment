from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("start"))
async def start(message: Message):
    await message.answer(
        f"Hello, {message.from_user.full_name}! I'll tell you when to buy or sell crypto, "
        f"to add coin type /add coin_symbol\n"
        f"for example: /add BTC (Any cases are allowed)"
    )
