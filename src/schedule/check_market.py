import asyncio
from datetime import datetime, timedelta

from aiogram import Bot
from sqlalchemy.orm import Session

from src.schedule.utils import collect_all_unique_coins


async def check_for_market_updates(minutes, session: Session, bot: Bot):
    while True:
        current_time = datetime.now()
        print(
            f"{current_time} - start checking for market updates every {minutes} minutes..."
        )
        target_time = current_time + timedelta(minutes=minutes)

        delta = target_time - current_time

        await asyncio.sleep(delta.seconds + 1)

        # here core logic

        print(collect_all_unique_coins(session))
