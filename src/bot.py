import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from sqlalchemy.orm import sessionmaker

from src.config import BOT_TOKEN
from src.database.models import Base, engine
from src.routers import start, add_coin, callbacks, list_coins, add_triger
from src.schedule.check_market import check_for_market_updates


async def main() -> None:
    dp = Dispatcher()
    dp.include_routers(
        start.router,
        list_coins.router,
        add_coin.router,
        add_triger.router,
        callbacks.router,
    )

    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    await bot.delete_webhook(drop_pending_updates=True)

    # Base.metadata.drop_all(bind=engine)  # if I forget to remove it - new db every reboot :/
    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    await asyncio.gather(
        dp.start_polling(bot, session=session),
        check_for_market_updates(1, session=session, bot=bot),
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
