#Author: Vodohleb04
from enum import Enum
from sqlalchemy import text
from collections import namedtuple


MessageBoxTitleMessagePair = namedtuple('MessageBoxTitleMessagePair', ['title', 'message'])


SCHEMA = 'orders_application'

ORDER_TABLE = 'order'

FORMAT_ENGINE_BASE = 'postgresql://{user}:{password}@localhost/postgres'

CREATE_BEFORE_UPDATE_OR_INSERT_TRIGGER_ORDER_CREATED_AT_COLUMN = text(f"""
CREATE FUNCTION {SCHEMA}.order_created_at_trigger_function() RETURNS trigger AS $$
    import datetime
    TD["new"]["created_at"] = datetime.datetime.now()
    return 'MODIFY'
$$ LANGUAGE plpython3u;
CREATE TRIGGER order_created_at_trigger BEFORE UPDATE OR INSERT ON {SCHEMA}.order FOR EACH ROW EXECUTE FUNCTION 
{SCHEMA}.order_created_at_trigger_function(); 
""")

DROP_BEFORE_UPDATE_OR_INSERT_TRIGGER_ORDER_CREATED_AT_COLUMN = text(f"""
DROP TRIGGER order_created_at_trigger on {SCHEMA}.{ORDER_TABLE};
DROP FUNCTION {SCHEMA}.order_created_at_trigger_function;
""")


class Icons(Enum):
    MainIcon = "./icons/bimer.jpg"
    MinusIcon = "./icons/minus.png"
    PlusIcon = "./icons/addIcon.png"


class StyleSheet(Enum):
    ToolTip = "QToolTip {background-color: white; color: black; border: black solid 1px};"
    MainWidgetBackground = "background-color: rgb(255, 250, 230);"
    ButtonBackground = "background-color: rgb(224, 224, 255);"
    EditBackground = "background-color: rgb(224, 224, 255);"
    WidgetWithItemsBackground = "background-color: rgb(255, 240, 254);"


class Titles(Enum):
    MainWindowTitle = "Заказы"
    RemoveOrderTitle = "Отменить заказ"
    AddOrderTitle = "Новый заказ"
    RejectOrderTitle = "Отмена"
    AcceptOrderTitle = "Заказать"
    FormatOrderPriceLabelTitle = "Итоговая стоимость: {:.2f}"
    OrdersCreatedAtHeader = "Время заказа"
    OrdersCustomerHeader = "Заказчик"
    OrdersAddressHeader = "Адрес"
    OrdersIdHeader = "Номер заказа"
    OrderItemsProductNameHeader = "Наименование товара"
    OrderItemsProductPriceHeader = "Стоимость товара"
    OrderItemsProductAmountHeader = "Количество"
    OrderItemsOrderPriceHeader = "Общая стоимость товара"
    OrderItemsProductIdHeader = "Каталожный номер"
    FormatOrderTabName = "Заказ {}"


class ToolTips(Enum):
    RemoveOrderTip = "Отменяет выбранный(-ые) заказ(-ы), Shift -"
    AddOrderTip = "Создать новый заказ, Shift +"
    RejectOrderTip = "Закрывает вкладку создания заказа, Esc"
    RemoveItemTip = "Убрать выбранный(-ые) продукт(-ы) из заказа, -"
    AddItemTip = "Добавить новый продукт в заказ, +"


class Shortcuts(Enum):
    RemoveOrderShortcut = "Shift+-"
    AddOrderShortcut = "Shift++"
    RejectOrderShortcut = "Esc"
    RemoveItemShortcut = "-"
    AddItemShortcut = "+"


class PlaceholderTexts(Enum):
    AddressEditText = "Введите адрес заказа..."


class BasicSizes(Enum):
    MainWindow = (1670, 700)


class OrdersModelErrorTypes(Enum):
    UnknownErrorOnServer = 0
    OrderNotDeleted = 1
    UnknownCollectionType = 2
    OrderItemNotDeleted = 3


class MessageBoxText(Enum):
    RemoveOrder = MessageBoxTitleMessagePair(
        title="Отмена заказов",
        message="Вы действительно хотите отменить выбранные заказы? (Отмена удалит выбранные заказы безвозвратно)."
    )
    OrderTabRejectOrder = MessageBoxTitleMessagePair(
        title="Отмена конструируемого заказа",
        message="Вы действительно хотите отменить оформление этого заказа и закрыть вкладку конструктора заказов? "
                "(Отмена безвозвратно удалит эту вкладку и всё её содержимое)."
    )
    FormatCloseTab = MessageBoxTitleMessagePair(
        title="Закрытие вкладки \"{}\" конструируемого заказа",
        message="Вы действительно хотите закрыть вкладу \"{}\" и отменить оформление заказа, конструируемого в ней? "
                "(Все указанные в ней данные будут безвозвратно удалены после закрытия вкладки)."
    )
    TabAccepted = MessageBoxTitleMessagePair(
        title="Оформление заказа",
        message="Вы подтверждаете, что хотите оформить этот заказ?"
    )
    OrderNotDeleted = MessageBoxTitleMessagePair(
        title='Заказ уже удалён',
        message='Не удалось удалить заказ с сервера, т.к. он уже удалён'
    )
    OrderItem = MessageBoxTitleMessagePair(
        title='Продукт уже удалён из заказа',
        message='Не удалось удалить продукт из заказа, т.к. он уже удалён скорее вссего уже удалён из заказа на сервере'
    )
    RemovingOrdersLen = MessageBoxTitleMessagePair(
        title="Ошибка при удалении заказов",
        message="При определении заказов для удаления произошла какая-то ошибка"
    )
    FormatRemovingOrderItemsLen = MessageBoxTitleMessagePair(
        title="Ошибка при удалении продуктов из заказа {}",
        message="При определении продуктов, удаляемых из заказа {}, произошла какая-то ошибка"
    )


class OrdersTableColumnIndex(Enum):
    OrderId = 0
    CreatedAt = 1
    Customer = 2
    Address = 3


class OrderItemsTableColumnIndexes(Enum):
    ProductName = 0
    ProductPrice = 1
    ProductAmount = 2
    TotalCostOfProductUnit = 3
    ProductId = 4
