#Author: Vodohleb04
from typing import Collection
from sqlalchemy import exc
from sqlalchemy import text, select, delete
from sqlalchemy import and_
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import selectinload, raiseload
from orders_i_model import OrdersIModel
from mapped_database import Order, OrderItem, Product
import config


class OrdersModel(OrdersIModel):
    # TODO сигналы об ошибках
    @staticmethod
    def _reserve_order_id_query(session: Session) -> int:
        return session.execute(text(f"SELECT nextval('{config.SCHEMA}.order_id_seq');")).scalar_one()

    @staticmethod
    def _remove_order_query(session: Session, order_id: int | Collection[int]) -> None:
        if isinstance(order_id, int):
            res = session.execute(delete(Order).where(Order.id == order_id).returning(Order.id))
            if not res.first():
                raise ValueError(config.MessageBoxText.OrderNotDeleted)
        elif isinstance(order_id, Collection):
            res = session.execute(delete(Order).where(Order.id.in_(order_id)).returning(Order.id))
            if not len(res.all()) == len(order_id):
                raise ValueError(config.MessageBoxText.OrderNotDeleted)
        else:
            raise TypeError(f"В качестве критерия для удаления заказов передан неизвестный тип данных. "
                            f"Ожидались int или Collection[int], но был получен {type(order_id)}")

    @staticmethod
    def _remove_order_items_query(session: Session, order_id: int, product_id: int | Collection[int]) -> None:
        if isinstance(product_id, int):
            res = session.execute(delete(OrderItem).where(
                  and_(
                      OrderItem.order_id == order_id,
                      OrderItem.product_id == product_id)
                  )
            )
            if not res.first():
                raise ValueError
        elif isinstance(product_id, Collection):
            res = session.execute(delete(OrderItem).where(
                  and_(
                      OrderItem.order_id == order_id,
                      OrderItem.product_id.in_(product_id))
                  )
            )
            if not len(res.all()) == len(product_id):
                raise ValueError(config.MessageBoxText.OrderNotDeleted)
        else:
            raise TypeError(f"В качестве критерия для удаления элементов заказа передан неизвестный тип данных. "
                            f"Ожидались int или Collection[int], но был получен {type(order_id)}")

    @staticmethod
    def _get_order_query(session: Session, order_id: int, selectin_relationship: bool) -> Order:
        if selectin_relationship:
            return session.scalar(select(Order)
                                  .where(Order.id == order_id)
                                  .options(selectinload(Order.products))
                                  )
        else:
            return session.scalar(select(Order)
                                  .where(Order.id == order_id)
                                  .options(raiseload(Order.products, sql_only=True))
                                  )

    @staticmethod
    def _get_product_query(session: Session, product_id: int, selectin_relationship: bool) -> Product:
        if selectin_relationship:
            return session.scalar(select(Product)
                                  .where(Product.id == product_id)
                                  .options(selectinload(Product.orders))
                                  )
        else:
            return session.scalar(select(Product)
                                  .where(Product.id == product_id)
                                  .options(raiseload(Product.orders, sql_only=True))
                                  )

    def reserve_order_id(self, user: str, password: str) -> int:
        with Session(create_engine(config.FORMAT_ENGINE_BASE.format(user=user, password=password))) as session:
            session.begin()
            try:
                new_order_id = self._reserve_order_id_query(session)
            except exc.SQLAlchemyError as ex:
                session.rollback()
                self.signalCommutator.ErrorOccurredSignal.emit(config.OrdersModelErrorTypes.UnknownErrorOnServer,
                                                               ex.args)
            else:
                session.commit()
                return new_order_id

    def remove_orders(self, order_id: int | Collection[int], user: str, password: str) -> None:
        with Session(create_engine(config.FORMAT_ENGINE_BASE.format(user=user, password=password))) as session:
            session.begin()
            try:
                self._remove_order_query(session, order_id)
            except exc.SQLAlchemyError as ex:
                session.rollback()
                self.signalCommutator.ErrorOccurredSignal.emit(config.OrdersModelErrorTypes.UnknownErrorOnServer,
                                                               ex.args)
            except TypeError as ex:
                self.signalCommutator.ErrorOccurredSignal.emit(config.OrdersModelErrorTypes.UnknownCollectionType,
                                                               ex.args)
            except ValueError as ex:
                self.signalCommutator.ErrorOccurredSignal.emit(config.OrdersModelErrorTypes.OrderNotDeleted,
                                                               ex.args)
                session.commit()
            else:
                session.commit()

    def add_order(self, order_id: int, address: str, user: str, password: str) -> None:
        with Session(create_engine(config.FORMAT_ENGINE_BASE.format(user=user, password=password))) as session:
            session.begin()
            try:
                session.add(Order(id=order_id, address=address, user_account=user))
            except exc.SQLAlchemyError as ex:
                session.rollback()
                self.signalCommutator.ErrorOccurredSignal.emit(config.OrdersModelErrorTypes.UnknownErrorOnServer,
                                                               ex.args)
            except TypeError as ex:
                self.signalCommutator.ErrorOccurredSignal.emit(config.OrdersModelErrorTypes.UnknownCollectionType,
                                                               ex.args)
            else:
                session.commit()

    def add_order_item(self, order_id: int, product_id: int, amount: int, user: str, password: str) -> None:
        with Session(create_engine(config.FORMAT_ENGINE_BASE.format(user=user, password=password))) as session:
            session.begin()
            try:
                session.add(OrderItem(order_id=order_id, product_id=product_id, product_amount=amount))
            except exc.SQLAlchemyError as ex:
                session.rollback()
                self.signalCommutator.ErrorOccurredSignal.emit(config.OrdersModelErrorTypes.UnknownErrorOnServer,
                                                               ex.args)
            except TypeError as ex:
                self.signalCommutator.ErrorOccurredSignal.emit(config.OrdersModelErrorTypes.UnknownCollectionType,
                                                               ex.args)
            else:
                session.commit()

    def remove_order_items(self, order_id: int, product_id: int | Collection[int], user: str, password: str) -> None:
        with Session(create_engine(config.FORMAT_ENGINE_BASE.format(user=user, password=password))) as session:
            session.begin()
            try:
                self._remove_order_items_query(session, order_id, product_id)
            except exc.SQLAlchemyError as ex:
                session.rollback()
                self.signalCommutator.ErrorOccurredSignal.emit(config.OrdersModelErrorTypes.UnknownErrorOnServer,
                                                               ex.args)
            except TypeError as ex:
                self.signalCommutator.ErrorOccurredSignal.emit(config.OrdersModelErrorTypes.UnknownCollectionType,
                                                               ex.args)
            except ValueError as ex:
                self.signalCommutator.ErrorOccurredSignal.emit(config.OrdersModelErrorTypes.OrderItemNotDeleted,
                                                               ex.args)
                session.commit()
            else:
                session.commit()

    def get_order(self, order_id: int, user: str, password: str, selectin_relationship=False) -> Order:
        with Session(create_engine(config.FORMAT_ENGINE_BASE.format(user=user, password=password))) as session:
            session.begin()
            try:
                return self._get_order_query(session, order_id, selectin_relationship)
            except exc.SQLAlchemyError as ex:
                self.signalCommutator.ErrorOccurredSignal.emit(config.OrdersModelErrorTypes.UnknownErrorOnServer,
                                                               ex.args)
            finally:
                session.close()

    def get_product(self, product_id: int, user: str, password: str, selectin_relationship:bool = False) -> Product:
        with Session(create_engine(config.FORMAT_ENGINE_BASE.format(user=user, password=password))) as session:
            session.begin()
            try:
                return self._get_product_query(session, product_id, selectin_relationship)
            except exc.SQLAlchemyError as ex:
                self.signalCommutator.ErrorOccurredSignal.emit(config.OrdersModelErrorTypes.UnknownErrorOnServer,
                                                               ex.args)
            finally:
                session.close()
