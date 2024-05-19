from typing import List

from sqlalchemy import DateTime, Float, String, Text, func, ForeignKey, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now(),
                                                 onupdate=func.now())


class Shop(Base):

    __tablename__ = 'shop'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    products: Mapped[List["Product"]] = relationship()


class ProductType(Base):

    __tablename__ = 'product_type'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    products: Mapped[List["Product"]] = relationship()


class Product(Base):

    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    link: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[int] = mapped_column(Float(asdecimal=True), nullable=False)
    price_credit: Mapped[int] =  mapped_column(Float(asdecimal=True), nullable=True)

    shop_id = mapped_column(ForeignKey('shop.id'))
    product_type_id = mapped_column(ForeignKey('product_type.id'))










