#Author: Vodohleb04
from PyQt5 import QtWidgets, QtGui, QtCore
from decimal import Decimal
import config


class OrderTab(QtWidgets.QWidget):

    def _make_grid_layout(self):
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName(f"tab{self.order_id}GridLayout")

    def _make_reject_order_button(self):
        self.rejectOrder = QtWidgets.QPushButton(self)
        self.rejectOrder.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.rejectOrder.setAutoFillBackground(False)
        self.rejectOrder.setStyleSheet(config.StyleSheet.ButtonBackground.value)
        self.rejectOrder.setObjectName(f"tab{self.order_id}RejectOrder")
        self.gridLayout.addWidget(self.rejectOrder, 2, 4, 1, 1)

    def _make_accept_order_button(self):
        self.acceptOrder = QtWidgets.QPushButton(self)
        self.acceptOrder.setEnabled(False)
        self.acceptOrder.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.acceptOrder.setAutoFillBackground(False)
        self.acceptOrder.setStyleSheet(config.StyleSheet.ButtonBackground.value)
        self.acceptOrder.setObjectName(f"tab{self.order_id}AcceptOrder")
        self.gridLayout.addWidget(self.acceptOrder, 2, 3, 1, 1)

    def _make_remove_item_button(self):
        self.removeItem = QtWidgets.QPushButton(self)
        self.removeItem.setEnabled(False)
        self.removeItem.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.removeItem.setToolTipDuration(5000)
        self.removeItem.setAutoFillBackground(False)
        self.removeItem.setStyleSheet(config.StyleSheet.ButtonBackground.value)
        self.removeItem.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(config.Icons.MinusIcon.value), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.removeItem.setIcon(icon1)
        self.removeItem.setObjectName(f"tab{self.order_id}RemoveItem")
        self.gridLayout.addWidget(self.removeItem, 1, 1, 1, 1)

    def _make_add_item_button(self):
        self.addItem = QtWidgets.QPushButton(self)
        self.addItem.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.addItem.setAutoFillBackground(False)
        self.addItem.setStyleSheet(config.StyleSheet.ButtonBackground.value)
        self.addItem.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(config.Icons.PlusIcon.value), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addItem.setIcon(icon2)
        self.addItem.setObjectName(f"tab{self.order_id}AddItem")
        self.gridLayout.addWidget(self.addItem, 1, 0, 1, 1)

    def _make_address_edit(self):
        self.addressEdit = QtWidgets.QLineEdit(self)
        self.addressEdit.setAutoFillBackground(False)
        self.addressEdit.setStyleSheet(config.StyleSheet.EditBackground.value)
        self.addressEdit.setInputMask("")
        self.addressEdit.setObjectName(f"tab{self.order_id}AddressEdit")
        self.gridLayout.addWidget(self.addressEdit, 2, 0, 1, 3)

    def _make_item_amount_edit(self):
        self.itemAmountEdit = QtWidgets.QSpinBox(self)
        self.itemAmountEdit.setEnabled(False)
        self.itemAmountEdit.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.itemAmountEdit.setAutoFillBackground(True)
        self.itemAmountEdit.setStyleSheet(config.StyleSheet.EditBackground.value)
        self.itemAmountEdit.setWrapping(False)
        self.itemAmountEdit.setFrame(True)
        self.itemAmountEdit.setObjectName(f"tab{self.order_id}ItemAmount")
        self.gridLayout.addWidget(self.itemAmountEdit, 1, 2, 1, 1)

    def _make_order_price_label(self):
        self.orderPriceLabel = QtWidgets.QLabel(self)
        self.orderPriceLabel.setAutoFillBackground(False)
        self.orderPriceLabel.setStyleSheet(config.StyleSheet.EditBackground.value)
        self.orderPriceLabel.setFrameShape(QtWidgets.QFrame.Box)
        self.orderPriceLabel.setFrameShadow(QtWidgets.QFrame.Plain)
        self.orderPriceLabel.setObjectName(f"tab{self.order_id}OrderPriceLabel")
        self.gridLayout.addWidget(self.orderPriceLabel, 1, 3, 1, 2)

    def _make_order_items_table_widget(self):
        self.orderItemsTableWidget = QtWidgets.QTableWidget(self)
        self._set_order_items_table_widget_options()
        self.orderItemsTableWidget.setColumnCount(5)
        self._set_order_items_table_widget_horizontal_headers()
        self.gridLayout.addWidget(self.orderItemsTableWidget, 0, 0, 1, 5)

    def _set_order_items_table_widget_options(self):
        self.orderItemsTableWidget.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.orderItemsTableWidget.setStyleSheet(config.StyleSheet.WidgetWithItemsBackground.value)
        self.orderItemsTableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.orderItemsTableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.orderItemsTableWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.orderItemsTableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.orderItemsTableWidget.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.orderItemsTableWidget.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.orderItemsTableWidget.setGridStyle(QtCore.Qt.SolidLine)
        self.orderItemsTableWidget.setCornerButtonEnabled(False)
        self.orderItemsTableWidget.setObjectName(f"tab{self.order_id}OrderItemsTableWidget")
        self.orderItemsTableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.orderItemsTableWidget.horizontalHeader().setStretchLastSection(False)
        self.orderItemsTableWidget.verticalHeader().setStretchLastSection(False)
        self.orderItemsTableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.orderItemsTableWidget.setEditTriggers(QtWidgets.QTableWidget.EditTrigger.NoEditTriggers)

    def _set_order_items_table_widget_horizontal_headers(self):
        for i in range(5):
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setBackground(QtGui.QColor(181, 181, 255))
            self.orderItemsTableWidget.setHorizontalHeaderItem(i, item)

    def _add_new_vertical_header(self):
        self.orderItemsTableWidget.setRowCount(self.orderItemsTableWidget.rowCount() + 1)
        vertical_header = QtWidgets.QTableWidgetItem()
        vertical_header.setTextAlignment(QtCore.Qt.AlignCenter)
        vertical_header.setBackground(QtGui.QColor(181, 181, 255))
        vertical_header.setText(str(self.orderItemsTableWidget.rowCount()))
        self.orderItemsTableWidget.setVerticalHeaderItem(self.orderItemsTableWidget.rowCount() - 1, vertical_header)

    def _emplace_order_item_product_name(self, product_name: str):
        brush = QtGui.QBrush(QtGui.QColor(239, 239, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        product_name_item = QtWidgets.QTableWidgetItem()
        product_name_item.setTextAlignment(QtCore.Qt.AlignCenter)
        product_name_item.setBackground(brush)
        product_name_item.setText(product_name)
        self.orderItemsTableWidget.setItem(
            self.orderItemsTableWidget.rowCount() - 1,
            config.OrderItemsTableColumnIndexes.ProductName.value,
            product_name_item
        )

    def _emplace_order_item_product_price(self, product_price: Decimal):
        brush = QtGui.QBrush(QtGui.QColor(239, 239, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        product_price_item = QtWidgets.QTableWidgetItem()
        product_price_item.setTextAlignment(QtCore.Qt.AlignCenter)
        product_price_item.setBackground(brush)
        product_price_item.setText("{:.2f}".format(product_price))
        self.orderItemsTableWidget.setItem(
            self.orderItemsTableWidget.rowCount() - 1,
            config.OrderItemsTableColumnIndexes.ProductPrice.value,
            product_price_item
        )

    def _emplace_order_item_product_amount(self, product_amount: int):
        brush = QtGui.QBrush(QtGui.QColor(239, 239, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        product_amount_item = QtWidgets.QTableWidgetItem()
        product_amount_item.setTextAlignment(QtCore.Qt.AlignCenter)
        product_amount_item.setBackground(brush)
        product_amount_item.setText(str(product_amount))
        self.orderItemsTableWidget.setItem(
            self.orderItemsTableWidget.rowCount() - 1,
            config.OrderItemsTableColumnIndexes.ProductAmount.value,
            product_amount_item
        )

    def _emplace_order_item_total_cost_of_product_unit(self, total_cost_of_product_unit: Decimal):
        brush = QtGui.QBrush(QtGui.QColor(239, 239, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        total_cost_of_product_unit_item = QtWidgets.QTableWidgetItem()
        total_cost_of_product_unit_item.setTextAlignment(QtCore.Qt.AlignCenter)
        total_cost_of_product_unit_item.setBackground(brush)
        total_cost_of_product_unit_item.setText("{:.2f}".format(total_cost_of_product_unit))
        self.orderItemsTableWidget.setItem(
            self.orderItemsTableWidget.rowCount() - 1,
            config.OrderItemsTableColumnIndexes.TotalCostOfProductUnit.value,
            total_cost_of_product_unit_item)

    def _emplace_order_item_product_id_unit(self, product_id: int):
        brush = QtGui.QBrush(QtGui.QColor(239, 239, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        product_id_item = QtWidgets.QTableWidgetItem()
        product_id_item.setTextAlignment(QtCore.Qt.AlignCenter)
        product_id_item.setBackground(brush)
        product_id_item.setText(str(product_id))
        self.orderItemsTableWidget.setItem(
            self.orderItemsTableWidget.rowCount() - 1,
            config.OrderItemsTableColumnIndexes.ProductId.value,
            product_id_item)

    def emplace_order_item(self,
                           product_name: str,
                           product_price: Decimal,
                           product_amount: int,
                           product_id: int):
        self._add_new_vertical_header()
        self._emplace_order_item_product_name(product_name)
        self._emplace_order_item_product_price(product_price)
        self._emplace_order_item_product_amount(product_amount)
        self._emplace_order_item_total_cost_of_product_unit(product_price * product_amount)
        self._emplace_order_item_product_id_unit(product_id)

    def update_price_label(self, order_price: Decimal):
        self.orderPriceLabel.setText(config.Titles.FormatOrderPriceLabelTitle.value.format(order_price))

    def remove_order_item_row(self, row_index: int):
        self.orderItemsTableWidget.removeRow(row_index)

    def _set_order_items_table_horizontal_headers(self):
        item = self.orderItemsTableWidget.horizontalHeaderItem(config.OrderItemsTableColumnIndexes.ProductName.value)
        item.setText(config.Titles.OrderItemsProductNameHeader.value)
        item = self.orderItemsTableWidget.horizontalHeaderItem(config.OrderItemsTableColumnIndexes.ProductPrice.value)
        item.setText(config.Titles.OrderItemsProductPriceHeader.value)
        item = self.orderItemsTableWidget.horizontalHeaderItem(config.OrderItemsTableColumnIndexes.ProductAmount.value)
        item.setText(config.Titles.OrderItemsProductAmountHeader.value)
        item = self.orderItemsTableWidget.horizontalHeaderItem(
            config.OrderItemsTableColumnIndexes.TotalCostOfProductUnit.value)
        item.setText(config.Titles.OrderItemsOrderPriceHeader.value)
        item = self.orderItemsTableWidget.horizontalHeaderItem(config.OrderItemsTableColumnIndexes.ProductId.value)
        item.setText(config.Titles.OrderItemsProductIdHeader.value)

    def _set_titles(self):
        self.acceptOrder.setText(config.Titles.AcceptOrderTitle.value)
        self.rejectOrder.setText(config.Titles.RejectOrderTitle.value)
        self.orderPriceLabel.setText(config.Titles.FormatOrderPriceLabelTitle.value.format(0))

    def _set_tool_tips(self):
        self.rejectOrder.setToolTip(config.ToolTips.RejectOrderTip.value)
        self.removeItem.setToolTip(config.ToolTips.RemoveItemTip.value)
        self.addItem.setToolTip(config.ToolTips.AddItemTip.value)

    def _set_shortcuts(self):
        self.rejectOrder.setShortcut(config.Shortcuts.RejectOrderShortcut.value)
        self.removeItem.setShortcut(config.Shortcuts.RemoveItemShortcut.value)
        self.addItem.setShortcut(config.Shortcuts.AddItemShortcut.value)

    def _set_objects_text_values(self):
        self.addressEdit.setPlaceholderText(config.PlaceholderTexts.AddressEditText.value)
        self._set_titles()
        self._set_tool_tips()
        self._set_shortcuts()
        self._set_order_items_table_horizontal_headers()

    def __init__(self, order_id: int, parent=None):
        super().__init__(parent=parent)
        self.order_id = order_id
        self.address_is_empty = True
        self.setObjectName(f"tab{self.order_id}")
        self._make_grid_layout()
        self._make_reject_order_button()
        self._make_accept_order_button()
        self._make_remove_item_button()
        self._make_add_item_button()
        self._make_address_edit()
        self._make_item_amount_edit()
        self._make_order_price_label()
        self._make_order_items_table_widget()
        self._set_objects_text_values()
