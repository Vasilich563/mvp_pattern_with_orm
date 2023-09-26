#Author: Vodohleb04
import threading
import config
from decimal import Decimal
from typing import List
from PyQt5.QtWidgets import QMessageBox
from orders_i_model import OrdersIModel
from orders_i_view import OrdersIView


class OrdersPresenter:

    def __init__(self, view: OrdersIView, model: OrdersIModel, user: str, password: str):
        self.view = view
        self.model = model
        self._connect_view_signals()
        self.user = user
        self.password = password

    def _connect_view_signals(self):
        self.view.signalCommutator.addOrderClickedSignal.connect(self._view_add_order_handler)
        self.view.signalCommutator.removeOrderClickedSignal.connect(self._view_remove_order_handler)
        self.view.signalCommutator.selectedOrdersChangedSignal.connect(self._view_selected_orders_changed_handler)
        self.view.signalCommutator.closeOrderTabSignal.connect(self._view_close_order_tab_handler)

    def _connect_order_tab(self, order_id):
        self.view.orderTabsDict[order_id].acceptOrder.clicked.connect(
            lambda: self._view_order_tab_accepted_handler(order_id))
        self.view.orderTabsDict[order_id].rejectOrder.clicked.connect(
            lambda: self._view_order_tab_rejected_handler(order_id))
        #self.view.orderTabsDict[order_id].addItem.clicked.connect(  # TODO обновление price label после вставки OrderItem
        #    lambda: self.signalCommutator.orderTabAddOrderItemClickedSignal.emit(order_id))
        self.view.orderTabsDict[order_id].removeItem.clicked.connect(
            lambda: self._view_order_tab_remove_order_item_handler(order_id))
        self.view.orderTabsDict[order_id].itemAmountEdit.valueChanged.connect(
            lambda: self._view_order_tab_item_amount_value_changed_handler(order_id))
        self.view.orderTabsDict[order_id].orderItemsTableWidget.itemSelectionChanged.connect(
            lambda: self._view_order_tab_selected_items_changed_handler(order_id))
        self.view.orderTabsDict[order_id].addressEdit.textChanged.connect(
            lambda: self._view_address_changed_handler(order_id)
        )

    def _view_add_order_handler(self):
        new_order_id = self.model.reserve_order_id(self.user, self.password)
        if not self.view.orderTabsDict:
            self.view.show_order_tabs_widget()
        self.view.add_order_tab(new_order_id)
        self._connect_order_tab(new_order_id)

    def _view_remove_order_handler(self):
        if self.view.get_question_box_result(
                config.MessageBoxText.RemoveOrder.value.title,
                config.MessageBoxText.RemoveOrder.value.message
        ) == QMessageBox.StandardButton.Yes:
            self._remove_selected_orders()

    def _define_removing_orders_table_rows(self) -> List[int]:
        removing_table_rows = []
        for i in range(0,
                       len(self.view.ordersTableWidget.selectedIndexes()),
                       self.view.ordersTableWidget.columnCount()):
            removing_table_rows.append(self.view.ordersTableWidget.selectedIndexes()[i].row())
        return removing_table_rows

    def _define_removing_orders_id(self, removing_table_rows: List[int]) -> List[int]:
        removing_orders_id = []
        for row in removing_table_rows:
            removing_orders_id.append(
                int(
                    self
                    .view
                    .ordersTableWidget
                    .item(row, config.OrdersTableColumnIndex.OrderId.value)
                    .text()
                )
            )
        return removing_orders_id

    def _check_amount_of_removing_orders(self, removing_table_rows: List[int], removing_orders_id: List[int]):
        if len(removing_orders_id) != len(removing_table_rows) or len(removing_orders_id) == 0:
            self.view.show_error_box(
                title=config.MessageBoxText.RemovingOrdersLen.value.title,
                message=config.MessageBoxText.RemovingOrdersLen.value.message
            )
            raise ValueError("Unknown error occurred")

    def _remove_orders_rows(self, removing_table_rows):
        removing_table_rows.sort(reverse=True)
        for row_index in removing_table_rows:
            self.view.remove_order_row(row_index)

    def _remove_selected_orders(self):
        removing_table_rows = self._define_removing_orders_table_rows()
        removing_orders_id = self._define_removing_orders_id(removing_table_rows)
        self._check_amount_of_removing_orders(removing_table_rows, removing_orders_id)

        if len(removing_table_rows) == 1:
            update_model = threading.Thread(
                target=self.model.remove_orders,
                args=(removing_orders_id[0], self.user, self.password)
            )
        else:
            update_model = threading.Thread(
                target=self.model.remove_orders,
                args=(removing_orders_id, self.user, self.password)
            )
        update_model.start()
        self._remove_orders_rows(removing_table_rows)

    def _view_selected_orders_changed_handler(self):
        if self.view.ordersTableWidget.selectedIndexes():
            self.view.set_remove_order_button_enabled(True)
        else:
            self.view.set_remove_order_button_enabled(False)

    def _view_order_tab_accepted_handler(self, order_id: int):
        question_box_result = self.view.get_question_box_result(config.MessageBoxText.TabAccepted.value.title,
                                                                config.MessageBoxText.TabAccepted.value.message)
        if question_box_result == QMessageBox.StandardButton.Yes:
            self.model.add_order(order_id,
                                 self.view.orderTabsDict[order_id].addressEdit.text(),
                                 self.user,
                                 self.password)
            make_order_items_thread = threading.Thread(target=self._make_order_items_for_order,
                                                       args=(order_id,))
            make_order_items_thread.start()
            order = self.model.get_order(order_id, self.user, self.password, selectin_relationship=False)
            self.view.emplace_order(order_id, order.created_at, order.user_account, order.address)
            make_order_items_thread.join()
            self._reject_order_tab(order_id)

    def _make_order_items_for_order(self, order_id: int):
        for i in range(self.view.orderTabsDict[order_id].orderItemsTableWidget.rowCount()):
            pr_id_idx = config.OrderItemsTableColumnIndexes.ProductId.value
            pr_amount_idx = config.OrderItemsTableColumnIndexes.ProductAmount.value
            product_id = int(self.view.orderTabsDict[order_id].orderItemsTableWidget.item(i, pr_id_idx).text())
            product_amount = int(self.view.orderTabsDict[order_id].orderItemsTableWidget.item(i, pr_amount_idx).text())
            self.model.add_order_item(order_id, product_id, product_amount, self.user, self.password)

    def _view_order_tab_rejected_handler(self, order_id: int):
        question_box_result = self.view.get_question_box_result(config.MessageBoxText.OrderTabRejectOrder.value.title,
                                                                config.MessageBoxText.OrderTabRejectOrder.value.message)
        if question_box_result == QMessageBox.StandardButton.Yes:
            self._reject_order_tab(order_id)

    def _define_removing_order_items_table_rows(self, order_id: int) -> List[int]:
        removing_table_rows = []
        for i in range(0,
                       len(self.view.orderTabsDict[order_id].orderItemsTableWidget.selectedIndexes()),
                       self.view.orderTabsDict[order_id].orderItemsTableWidget.columnCount()):
            removing_table_rows.append(
                self.view.orderTabsDict[order_id].orderItemsTableWidget.selectedIndexes()[i].row()
            )
        return removing_table_rows

    def _define_removing_product_id(self, order_id: int, removing_table_rows: List[int]) -> List[int]:
        removing_product_id = []
        for row in removing_table_rows:
            removing_product_id.append(
                int(self
                    .view
                    .orderTabsDict[order_id]
                    .orderItemsTableWidget
                    .item(row, config.OrderItemsTableColumnIndexes.ProductId.value)
                    .text()
                    )
            )
        return removing_product_id

    def _remove_order_items_rows(self, order_id: int, removing_table_rows: List[int]):
        removing_table_rows.sort(reverse=True)
        for row_index in removing_table_rows:
            self.view.orderTabsDict[order_id].remove_order_item_row(row_index)

    def _check_amount_of_removing_order_items(self,
                                              order_id: int,
                                              removing_product_id: List[int],
                                              removing_table_rows: List[int]) -> None:
        if len(removing_product_id) != len(removing_table_rows) or len(removing_product_id) == 0:
            self.view.show_error_box(
                title=config.MessageBoxText.FormatRemovingOrderItemsLen.value.title.format(order_id),
                message=config.MessageBoxText.FormatRemovingOrderItemsLen.value.message.format(order_id))
            raise ValueError("Unknown error occurred")

    def _view_order_tab_remove_order_item_handler(self, order_id: int):
        removing_table_rows = self._define_removing_order_items_table_rows(order_id)
        removing_product_id = self._define_removing_product_id(order_id, removing_table_rows)
        self._define_add_order_enable(
            order_id, self.view.orderTabsDict[order_id].orderItemsTableWidget.rowCount() - len(removing_product_id)
        )
        self._check_amount_of_removing_order_items(order_id, removing_product_id, removing_table_rows)

        if len(removing_product_id) == 1:
            update_model = threading.Thread(
                target=self.model.remove_order_items,
                args=(order_id, removing_product_id[0], self.user, self.password))
        else:
            update_model = threading.Thread(
                target=self.model.remove_order_items,
                args=(order_id, removing_product_id, self.user, self.password))
        update_model.start()
        self._remove_order_items_rows(order_id, removing_table_rows)

    def _view_order_tab_item_amount_value_changed_handler(self, order_id: int):
        # TODO if value > available
        new_item_amount = self.view.orderTabsDict[order_id].itemAmountEdit.value()
        current_row_index = self.view.orderTabsDict[order_id].orderItemsTableWidget.currentRow()
        item_price = Decimal(self.view.orderTabsDict[order_id].orderItemsTableWidget.item(
            current_row_index, config.OrderItemsTableColumnIndexes.ProductPrice.value).text())
        self.view.orderTabsDict[order_id].orderItemsTableWidget.item(
            current_row_index, config.OrderItemsTableColumnIndexes.ProductAmount.value).setText(str(new_item_amount))
        self.view.orderTabsDict[order_id].orderItemsTableWidget.item(
            current_row_index, config.OrderItemsTableColumnIndexes.TotalCostOfProductUnit.value
        ).setText("{:.2f}".format(item_price * new_item_amount))
        self.view.orderTabsDict[order_id].update_price_label(self._count_order_price(order_id))

    def _count_order_price(self, order_id: int) -> Decimal:
        order_price = Decimal(0)
        for i in range(self.view.orderTabsDict[order_id].orderItemsTableWidget.rowCount()):
            item_amount = int(self.view.orderTabsDict[order_id].orderItemsTableWidget.item(
                i, config.OrderItemsTableColumnIndexes.ProductAmount.value).text())
            item_price = Decimal(self.view.orderTabsDict[order_id].orderItemsTableWidget.item(
                i, config.OrderItemsTableColumnIndexes.ProductPrice.value).text())
            order_price += item_price * item_amount
        return order_price

    def _reject_order_tab(self, order_id: int):
        self.view.remove_order_tab_from_widget(
            self.view.orderTabsWidget.indexOf(self.view.orderTabsDict[order_id])
        )
        self.view.orderTabsDict.pop(order_id)
        if not self.view.orderTabsDict:
            self.view.hide_order_tabs_widget()

    def _view_order_tab_selected_items_changed_handler(self, order_id: int):
        column_count = self.view.orderTabsDict[order_id].orderItemsTableWidget.columnCount()
        if len(self.view.orderTabsDict[order_id].orderItemsTableWidget.selectedIndexes()) / column_count > 1:
            self.view.orderTabsDict[order_id].removeItem.setEnabled(True)
            self.view.orderTabsDict[order_id].itemAmountEdit.setEnabled(False)
            self.view.orderTabsDict[order_id].itemAmountEdit.setValue(0)
        elif len(self.view.orderTabsDict[order_id].orderItemsTableWidget.selectedIndexes()) / column_count == 1:
            self.view.orderTabsDict[order_id].removeItem.setEnabled(True)
            self.view.orderTabsDict[order_id].itemAmountEdit.setEnabled(True)
            current_row = self.view.orderTabsDict[order_id].orderItemsTableWidget.currentRow()
            current_item_amount = int(self.view.orderTabsDict[order_id].orderItemsTableWidget.item(
                current_row, config.OrderItemsTableColumnIndexes.ProductAmount.value).text())
            self.view.orderTabsDict[order_id].itemAmountEdit.setValue(current_item_amount)
        else:
            self.view.orderTabsDict[order_id].removeItem.setEnabled(False)
            self.view.orderTabsDict[order_id].itemAmountEdit.setEnabled(False)

    def _view_address_changed_handler(self, order_id: int):
        if self.view.orderTabsDict[order_id].addressEdit.text():
            if self.view.orderTabsDict[order_id].address_is_empty:
                self.view.orderTabsDict[order_id].address_is_empty = False
        else:
            self.view.orderTabsDict[order_id].address_is_empty = True
        self._define_add_order_enable(order_id, self.view.orderTabsDict[order_id].orderItemsTableWidget.rowCount())

    def _view_close_order_tab_handler(self, order_tab_index: int):
        question_box_result = self.view.get_question_box_result(
            config.MessageBoxText.FormatCloseTab.value.title.format(
                self.view.orderTabsWidget.tabText(order_tab_index)),
            config.MessageBoxText.FormatCloseTab.value.message.format(
                self.view.orderTabsWidget.tabText(order_tab_index))
        )
        if question_box_result == QMessageBox.StandardButton.Yes:
            order_id = self.view.orderTabsWidget.widget(order_tab_index).order_id
            self.view.remove_order_tab_from_widget(order_tab_index)
            self.view.orderTabsDict.pop(order_id)
            if not self.view.orderTabsDict:
                self.view.hide_order_tabs_widget()

    def _define_add_order_enable(self, order_id: int, order_items_amount: int):
        add_order_enabled = (not self.view.orderTabsDict[order_id].address_is_empty and bool(order_items_amount))
        if self.view.orderTabsDict[order_id].acceptOrder.isEnabled() != add_order_enabled:
            self.view.orderTabsDict[order_id].acceptOrder.setEnabled(add_order_enabled)
