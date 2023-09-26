#Author: Vodohleb04
from PyQt5 import QtCore


class OrdersIViewSignalsCommutator(QtCore.QObject):
    addOrderClickedSignal = QtCore.pyqtSignal()
    removeOrderClickedSignal = QtCore.pyqtSignal()
    selectedOrdersChangedSignal = QtCore.pyqtSignal()
    closeOrderTabSignal = QtCore.pyqtSignal(int)
