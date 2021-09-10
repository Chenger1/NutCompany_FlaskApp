from enum import Enum


class UserTypeChoice(Enum):
    legal_person = 'Юридическое лицо'
    physical_person = 'Физические лицо'


class DeliveryTypeChoice(Enum):
    new_mail = 'Новая почта (по Украине, оплата за счет Клиента)'
    courier = 'Куръер по Одесса'
    self_pickup = 'Самовывоз со склада'


class PaymentChoice(Enum):
    privat = 'LiqPay/Приват24'
    cashless = 'Безналичный расчет'
    cash = 'Наличными при получении (Наложенным платежом)'


class OrderStatusChoice(Enum):
    unpaid = 'Неоплачен'
    in_progress = 'В обработке'
    sent = 'Отправлен'
    done = 'Выполнен'


class RequestStatusChoice(Enum):
    in_progress = 'В обработке'
    closed = 'Отказано'
    done = 'Выполнен'
