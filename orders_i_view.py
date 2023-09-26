#Author: Vodohleb04
from PyQt5.QtWidgets import QMessageBox
from typing import Dict
from abc import ABC, abstractmethod
from datetime import datetime
from orders_i_view_signals_commutator import OrdersIViewSignalsCommutator
from order_tab import OrderTab


class OrdersIView(ABC):
    def __init__(self):
        self.ordersTableWidget = None
        self.orderTabsWidget = None
        self.signalCommutator = OrdersIViewSignalsCommutator()
        self.orderTabsDict: Dict[int, OrderTab] = {}

    @abstractmethod
    def _make_remove_order_button(self):
        raise NotImplementedError

    @abstractmethod
    def _make_add_order_button(self):
        raise NotImplementedError

    @abstractmethod
    def _make_orders_table_widget(self):
        raise NotImplementedError

    @abstractmethod
    def emplace_order(self, order_id: int, created_at: datetime, customer: str, address: str):
        raise NotImplementedError

    @abstractmethod
    def remove_order_row(self, row_index: int):
        raise NotImplementedError

    @abstractmethod
    def _make_order_tabs_widget(self):
        raise NotImplementedError

    @abstractmethod
    def add_order_tab(self, order_id: int):
        raise NotImplementedError

    @abstractmethod
    def remove_order_tab_from_widget(self, tab_index: int):
        raise NotImplementedError

    @abstractmethod
    def set_remove_order_button_enabled(self, enabled_flag: bool):
        raise NotImplementedError

    @abstractmethod
    def get_question_box_result(self, title: str, message: str) -> QMessageBox.StandardButton:
        raise NotImplementedError

    @abstractmethod
    def show_error_box(self, title: str, message: str):
        raise NotImplementedError

    @abstractmethod
    def hide_order_tabs_widget(self):
        raise NotImplementedError

    @abstractmethod
    def show_order_tabs_widget(self):
        raise NotImplementedError
