#Author: Vodohleb04
from __future__ import annotations
from typing import Iterable
from abc import ABC, abstractmethod
from mapped_database import Order, Product
from orders_i_model_signals_commutator import OrdersIModelSignalsCommutator


class OrdersIModel(ABC):
    def __init__(self):
        self.signalCommutator = OrdersIModelSignalsCommutator()

    @abstractmethod
    def reserve_order_id(self, user: str, password: str) -> int:
        raise NotImplementedError

    @abstractmethod
    def remove_orders(self, order_id: int | Iterable[int], user: str, password: str):
        raise NotImplementedError

    @abstractmethod
    def add_order(self, order_id: int, address: str, user: str, password: str):
        raise NotImplementedError

    @abstractmethod
    def add_order_item(self, order_id: int, product_id: int, amount: int, user: str, password: str):
        raise NotImplementedError

    @abstractmethod
    def remove_order_items(self, order_id: int, product_id: int | Iterable[int], user: str, password: str):
        raise NotImplementedError

    @abstractmethod
    def get_order(self, order_id: int, user: str, password: str, selectin_relationship: bool = False) -> Order:
        raise NotImplementedError

    @abstractmethod
    def get_product(self, product_id: int, user: str, password: str, selectin_relationship:bool = False) -> Product:
        raise NotImplementedError
