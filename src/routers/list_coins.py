from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.models import CoinRecord

router = Router()


@router.message(Command("list"))
async def return_coins(message: Message, session: Session):
    selected_coins = session.scalars(
        select(CoinRecord)
        .where(CoinRecord.user_id == message.from_user.id)
        .join(CoinRecord.triggers, full=True)
        .group_by(CoinRecord)
    ).all()

    print(
        select(CoinRecord)
        .where(CoinRecord.user_id == message.from_user.id)
        .join(CoinRecord.triggers, full=True)
        .group_by(CoinRecord)
    )

    if not selected_coins:
        await message.answer("You have no coins, learn how to add one!\n\n/start")
        return

    text = "Your coins and triggers:\n\n"
    for coin in selected_coins:
        text += (
            f"<b>{coin.coin_symbol}:</b>\n" f"Last price: {coin.last_price_usd} USD\n"
        )
        for trigger in coin.triggers:
            text += f"{trigger.trigger_usd} USD\n"
        text += "\n"

    await message.answer(text)
