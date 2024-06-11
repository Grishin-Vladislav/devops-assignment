from sqlalchemy import (
    ForeignKey,
    BIGINT,
)
from sqlalchemy import create_engine
from sqlalchemy.orm import (
    declarative_base,
    relationship,
    mapped_column,
    Mapped,
)

from src.config import PG_USER, PG_PASS, PG_NAME

# No async driver, no alembic, no normalization, one session - MVP


db_url = f"postgresql+psycopg2://{PG_USER}:{PG_PASS}@postgres_db/{PG_NAME}"
engine = create_engine(db_url, echo=False)

Base = declarative_base()


class CoinRecord(Base):
    __tablename__ = "coin"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BIGINT)
    coin_symbol: Mapped[str]
    external_coin_id: Mapped[int]
    last_price_usd: Mapped[float]

    triggers = relationship(
        "Trigger", back_populates="coin", cascade="all, delete-orphan"
    )


class Trigger(Base):
    __tablename__ = "trigger"

    id: Mapped[int] = mapped_column(primary_key=True)
    coin_record_id: Mapped[int] = mapped_column(ForeignKey("coin.id"))
    trigger_usd: Mapped[float]

    coin = relationship("CoinRecord", back_populates="triggers")
