from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder


from src.utils.coin_api import return_coin_info_or_status_code

router = Router()


@router.message(Command("add"))
async def add_coin_to_list(message: Message, command: CommandObject):
    if command.args is None:
        await message.answer(
            "You should add coin name after command. For example: /add btc"
        )
        return

    coin_symbol_from_user = command.args.upper()

    external_coin_info: dict = return_coin_info_or_status_code(
        coin_symbol=coin_symbol_from_user
    )

    if external_coin_info.get("error"):
        if external_coin_info["error"] == 400:
            await message.answer("Coin not found. Please check spelling and try again")
            return
        else:
            await message.answer(
                f"So, There was something wrong with api call."
                f"\n\n It was not successful and returned this status code.\n"
                f'<b>{external_coin_info["error"]}</b>'
                f"\n\n Please try again later."
            )
            return

    coin_id = external_coin_info["id"]
    coin_symbol = external_coin_info["symbol"]
    coin_name = external_coin_info["name"]

    builder = InlineKeyboardBuilder()
    builder.button(text="Yes", callback_data=f"add_coin_yes {coin_id} {coin_symbol}")
    builder.button(text="No", callback_data=f"add_coin_no {coin_id} {coin_symbol}")

    await message.answer(
        f"symbol: <b>{coin_symbol}</b>\n"
        f"name: <b>{coin_name}</b>\n\n"
        f"<b>is this your coin?</b>",
        reply_markup=builder.as_markup(),
    )
