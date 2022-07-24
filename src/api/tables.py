from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Date,
    DECIMAL,
    BigInteger,
    ForeignKey,
    text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    emoji = Column(String(1), nullable=True)


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    date = Column(Date(), nullable=False, server_default=text("now()::date"))
    is_expense = Column(Boolean(), nullable=False)
    amount = Column(DECIMAL(10, 2, asdecimal=True), nullable=False)
    comment = Column(String(255), nullable=True, index=True)
    category_id = Column(Integer(), ForeignKey("categories.id"), nullable=False)
    user_id = Column(BigInteger(), ForeignKey("users.id"), nullable=False)

    category = relationship("Category")


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger(), primary_key=True)  # telegram id
    username = Column(String(32), nullable=True)
    balance = Column(DECIMAL(10, 2, asdecimal=True), nullable=False, server_default=text("0.00::numeric"))

    expenses = relationship("Expense")
