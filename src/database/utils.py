from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.models import CoinRecord, Trigger


def commit_session(session: Session):
    try:
        session.commit()
    except Exception as e:  # silly but fast solution
        print(e)
        session.rollback()


def add_coin_to_db(coin_record: CoinRecord, session: Session):
    session.add(coin_record)
    commit_session(session)


def get_all_triggers_for_coin(coin: CoinRecord, session: Session):
    return session.scalars(
        select(Trigger).where(Trigger.coin_record_id == coin.id)
    ).all()


def get_coin_from_db_or_none(coin_symbol: str, session: Session):
    return session.scalars(
        select(CoinRecord).where(CoinRecord.coin_symbol == coin_symbol)
    ).first()


def add_triggers_to_db(triggers: list[float], coin: CoinRecord, session: Session):
    old_trigger_objs = get_all_triggers_for_coin(coin=coin, session=session)
    old_triggers = [trigger.trigger_usd for trigger in old_trigger_objs]
    new_triggers = [
        Trigger(trigger_usd=trigger, coin=coin)
        for trigger in set(triggers)
        if trigger not in old_triggers
    ]
    session.add_all(new_triggers)
    commit_session(session)
