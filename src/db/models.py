from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, Float, String, DateTime, func
from datetime import datetime
from sqlalchemy import ForeignKey, JSON

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Preferences(Base):
    __tablename__ = "preferences"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    allergies: Mapped[list | None] = mapped_column(JSON, nullable=True)
    likes: Mapped[list | None] = mapped_column(JSON, nullable=True)
    dislikes: Mapped[list | None] = mapped_column(JSON, nullable=True)
    dietary_preferences: Mapped[list | None] = mapped_column(JSON, nullable=True)


class RefreshTokens(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    token_hash: Mapped[str] = mapped_column(String)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class OrderHistory(Base):
    __tablename__ = "order_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    dish_id: Mapped[int] = mapped_column(Integer)
    dish_name: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(Float)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    ingredients: Mapped[list | None] = mapped_column(JSON, nullable=True)
    reason: Mapped[str | None] = mapped_column(String, nullable=True)
    ordered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class Dislikes(Base):
    __tablename__ = "dislikes"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    dish_id: Mapped[int] = mapped_column(Integer, primary_key=True)