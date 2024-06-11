from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.models import CoinRecord, Trigger


def collect_all_unique_coins(session: Session):
    return session.scalars(
        select(CoinRecord).distinct(CoinRecord.external_coin_id)
    ).all()


def collect_all_unique_triggers_for_coin(session: Session, coin: CoinRecord):
    return session.scalars(
        select(Trigger)
        .distinct(Trigger.trigger_usd)
        .where(Trigger.coin_record_id == coin.id)
    )
