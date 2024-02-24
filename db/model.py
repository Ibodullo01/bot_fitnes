
from sqlalchemy import BIGINT
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    chat_id: Mapped[int] = mapped_column(__type_pos=BIGINT,primary_key=True)
    username: Mapped[str]






