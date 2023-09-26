# Author: Vodohleb04
from __future__ import annotations
from decimal import Decimal
from datetime import datetime
from typing import List
from sqlalchemy import MetaData
from sqlalchemy import VARCHAR, TIMESTAMP, NUMERIC
from sqlalchemy import ForeignKey, CheckConstraint
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import validates

import config


class ServerBase(DeclarativeBase):
    metadata = MetaData(schema='orders_application')

    type_annotation_map = {
        Decimal: NUMERIC,
        str: VARCHAR,
        datetime: TIMESTAMP(timezone=False)
    }

    @classmethod
    def create_all_from_metadata(cls, engine):
        cls.metadata.create_all(engine)


class Order(ServerBase):
    __tablename__ = 'order'

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    address: Mapped[str]
    user_account: Mapped[str]

    products: Mapped[List[OrderItem]] = relationship(back_populates='order')

    def __repr__(self) -> str:
        return (f"Order(id={self.id}, created_at={self.created_at}, "
                f"address={self.address}, user_account={self.user_account})")


class Product(ServerBase):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str]
    amount: Mapped[int] = mapped_column("available amount", nullable=False)
    price: Mapped[Decimal]

    orders: Mapped[List[OrderItem]] = relationship(back_populates="product", cascade='all, delete')

    __table_args__ = (
        CheckConstraint("\"available amount\" > 0"),
        CheckConstraint("price > 0")
    )

    @validates("amount")
    def check_amount(self, key, amount):
        if amount < 0:
            raise ValueError("Количество товара не может быть меньше 0")
        return amount

    @validates("price")
    def check_price(self, key, price):
        if price < Decimal(0.01):
            raise ValueError("Цена за единицу товара не может быть меньше 0.01$")
        return price

    def __repr__(self) -> str:
        return f"Product(id={self.id}, product_name={self.product_name}, amount={self.amount}, price={self.price})"


class OrderItem(ServerBase):
    __tablename__ = 'order_item'

    order_id: Mapped[int] = mapped_column("order id",
                                          ForeignKey("order.id", ondelete='CASCADE'),
                                          primary_key=True,
                                          nullable=False)
    product_id: Mapped[int] = mapped_column("product id",
                                            ForeignKey("product.id"),
                                            primary_key=True,
                                            nullable=False)
    product_amount: Mapped[int] = mapped_column("product amount", nullable=False)

    order: Mapped[Order] = relationship(back_populates='products', passive_deletes=True)
    product: Mapped[Product] = relationship(back_populates='orders', passive_deletes=True)

    __table_args__ = (CheckConstraint("\"product amount\" > 0"),)

    @validates("product_amount")
    def check_product_amount(self, key, product_amount):
        if product_amount <= 0:
            raise ValueError("Невозможно заказать товар в количестве меньшем, чем 1 ед.")
        return product_amount

    def __repr__(self) -> str:
        return (f"OrderItem(order_id={self.order_id}, product_id={self.product_id}, "
                f"product_amount={self.product_amount})")

