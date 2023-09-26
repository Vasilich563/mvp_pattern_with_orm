#Author: Vodohleb04
from PyQt5 import QtCore
from config import OrdersModelErrorTypes


class OrdersIModelSignalsCommutator(QtCore.QObject):
    ErrorOccurredSignal = QtCore.pyqtSignal(OrdersModelErrorTypes, tuple)
