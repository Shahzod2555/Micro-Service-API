from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from src.core.models.base import Base


class AuthUser(Base):
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(12), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
