from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.orm import Session

from src.database.models import CoinRecord
from src.database.utils import add_coin_to_db
from src.utils.coin_api import check_coin_price_or_status_code

router = Router()


# needs refactoring for duplicates
@router.callback_query(F.data.startswith("add_coin_yes"))
async def resolve_adding_coin_to_db(call: CallbackQuery, session: Session):
    await call.answer()
    await call.message.edit_reply_markup()

    current_coin_price = check_coin_price_or_status_code(call.data.split()[1])
    if current_coin_price.get("error"):
        await call.message.answer(
            f"So, There was something wrong with api call."
            f"At this step coin was found but second api call for checking price "
            f"was not successful and returned this status code.\n"
            f'<b>{current_coin_price["error"]}</b>'
            f"\n\n Please try again later."
        )
        return
    current_coin_price = current_coin_price["price"]  # silly

    coin_record = CoinRecord(
        user_id=call.from_user.id,
        external_coin_id=call.data.split()[1],
        coin_symbol=call.data.split()[2],
        last_price_usd=current_coin_price,
    )

    add_coin_to_db(coin_record, session)

    await call.message.answer(
        f"Coin {call.data.split()[2]} added to you list, to see your coins use /list\n\n"
        f"But it is useless unless you add triggers to it...\n"
        f"Type /addtriggers {call.data.split()[2]} 25 50 100 to add"
        f" triggers 25, 50, 100 to {call.data.split()[2]}\n\n"
        f"coin name is case <b>insensitive</b>"
    )


@router.callback_query(F.data.startswith("add_coin_no"))
async def resolve_adding_coin_to_db(call: CallbackQuery):
    await call.answer()
    await call.message.edit_reply_markup()
    await call.message.answer(f"ok, better luck next time!")
