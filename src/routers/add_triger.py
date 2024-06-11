from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from sqlalchemy.orm import Session

from src.database.models import CoinRecord
from src.database.utils import get_coin_from_db_or_none, add_triggers_to_db

router = Router()


@router.message(Command("addtriggers"))
async def add_triggers(message: Message, command: CommandObject, session: Session):
    if command.args is None or len(command.args.split(" ")) < 2:
        await message.answer(
            "You should add coin name and triggers after command.\n"
            "For example: /addtriggers btc 666 777 111 222 444\n"
            "This will add triggers 666, 777, 111, 222, 444 to btc "
            "(coin symbol is case insensitive)"
        )
        return

    coin_symbol_from_user = command.args.split(" ")[0].upper()
    triggers = command.args.split(" ")[1:]

    coin: CoinRecord = get_coin_from_db_or_none(
        coin_symbol=coin_symbol_from_user, session=session
    )

    if not coin:
        await message.answer(
            "Coin not found in your list. Please check spelling and try again\n"
            "Also check if coin is added to list with /list command"
        )
        return

    try:
        float_triggers = [float(x) for x in triggers]
        assert all(0 < float_trigger <= 1000000 for float_trigger in float_triggers)
    except ValueError:
        await message.answer("Triggers should be numbers. Please check and try again")
        return
    except AssertionError:
        await message.answer(
            "Triggers should be less than 1000000 and greater than 0. "
            "Please check and try again"
        )
        return

    add_triggers_to_db(triggers=float_triggers, coin=coin, session=session)

    await message.answer(f"Triggers for {coin.coin_symbol} added successfully")
